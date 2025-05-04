from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import django_filters
from .forms import NewsForm
from .models import Post, Author, Category
from .filters import PostFilter, UserNewsFilter
from rest_framework import viewsets, permissions
from .serializers import PostSerializer
from django.shortcuts import redirect, render, get_object_or_404
from datetime import datetime, timedelta
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
import pytz


class NewsList(ListView):
    model = Post
    ordering = '-date_creation'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Считываем выбранный часовой пояс из сессии или по умолчанию UTC
        timezone_name = self.request.session.get('django_timezone', 'UTC')
        user_timezone = pytz.timezone(timezone_name)  # Получаем объект часового пояса

        # Получаем текущее время в UTC и переводим в часовой пояс пользователя
        current_time = timezone.now().astimezone(user_timezone)  # Переводим время в выбранный часовой пояс

        # Делаем проверку времени для смены фона
        time_of_day = "day" if 7 <= current_time.hour < 19 else "night"

        context['is_author'] = self.request.user.is_authenticated and self.request.user.groups.filter(name='authors').exists()
        context['current_time'] = current_time  # Добавляем время в контекст
        context['time_of_day'] = time_of_day  # Добавляем информацию о времени суток
        context['date_creation'] = datetime.utcnow()

        if self.request.user.is_authenticated and context['is_author']:
            limit = settings.DAY_LIMIT_POSTS
            prev_day = timezone.now() - timedelta(hours=24)
            posts_day_count = Post.objects.filter(
                date_creation__gte=prev_day,
                author__authorUser=self.request.user
            ).count()

            context.update({
                'limit': limit,
                'count': posts_day_count,
                'posts_limit': posts_day_count >= limit,
            })
        else:
            context.update({'limit': 0, 'count': 0, 'posts_limit': False})

        context['timezones'] = pytz.common_timezones  # Добавляем список всех часовых поясов

        return context

    def post(self, request):
        # Получаем новый часовой пояс из формы
        timezone_name = request.POST.get('timezone', 'UTC')

        # Если выбранный часовой пояс правильный, сохраняем его в сессии и активируем
        if timezone_name in pytz.common_timezones:
            request.session['django_timezone'] = timezone_name
            timezone.activate(pytz.timezone(timezone_name))

        # После изменения часового пояса пересчитываем время и обновляем контекст
        return redirect(request.path)


class NewList(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'

    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs): # переопределяем метод получения объекта
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        # если объекта нет в кэше, то получаем его и записывает в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Считываем выбранный часовой пояс из сессии
        timezone_name = self.request.session.get('django_timezone', 'UTC')
        timezone.activate(pytz.timezone(timezone_name))  # Активируем часовой пояс
        current_time = timezone.now()  # Получаем текущее время

        context['timezones'] = pytz.common_timezones  # Все доступные часовые пояса
        context['current_time'] = current_time  # Добавляем в контекст текущее время
            
        return context    


class UserNewsListView(ListView):
    model = Post
    template_name = 'user_news.html'
    context_object_name = 'user_news'
    paginate_by = 10

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Post.objects.none()

        author = getattr(self.request.user, 'author', None)
        if not author:
            return Post.objects.none()

        queryset = Post.objects.filter(author=author).order_by('-date_creation')
        self.filterset = UserNewsFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Считываем выбранный часовой пояс из сессии
        timezone_name = self.request.session.get('django_timezone', 'UTC')
        timezone.activate(pytz.timezone(timezone_name))  # Активируем часовой пояс
        current_time = timezone.now()  # Получаем текущее время

        context['filterset'] = self.filterset
        context['timezones'] = pytz.common_timezones  # Все доступные часовые пояса
        context['current_time'] = current_time  # Добавляем в контекст текущее время

        return context


class NewsSearch(ListView):
    model = Post
    ordering = '-date_creation'
    template_name = 'news_search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['is_author'] = self.request.user.is_authenticated and self.request.user.groups.filter(name='authors').exists()
        
        # Считываем выбранный часовой пояс из сессии
        timezone_name = self.request.session.get('django_timezone', 'UTC')
        timezone.activate(pytz.timezone(timezone_name))  # Активируем часовой пояс
        current_time = timezone.now()  # Получаем текущее время

        context['timezones'] = pytz.common_timezones  # Все доступные часовые пояса
        context['current_time'] = current_time  # Добавляем в контекст текущее время

        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = NewsForm
    model = Post
    template_name = 'new_edit.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        author, _ = Author.objects.get_or_create(authorUser=self.request.user)
        self.object.author = author
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Считываем выбранный часовой пояс из сессии
        timezone_name = self.request.session.get('django_timezone', 'UTC')
        timezone.activate(pytz.timezone(timezone_name))  # Активируем часовой пояс
        current_time = timezone.now()  # Получаем текущее время

        context['timezones'] = pytz.common_timezones  # Все доступные часовые пояса
        context['current_time'] = current_time  # Добавляем в контекст текущее время
            
        return context   


class NewsEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)  
    form_class = NewsForm
    model = Post
    template_name = 'new_edit.html'
    success_url = reverse_lazy('user_news')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Считываем выбранный часовой пояс из сессии
        timezone_name = self.request.session.get('django_timezone', 'UTC')
        timezone.activate(pytz.timezone(timezone_name))  # Активируем часовой пояс
        current_time = timezone.now()  # Получаем текущее время

        context['timezones'] = pytz.common_timezones  # Все доступные часовые пояса
        context['current_time'] = current_time  # Добавляем в контекст текущее время
            
        return context   


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'new_delete.html'
    success_url = reverse_lazy('news_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Считываем выбранный часовой пояс из сессии
        timezone_name = self.request.session.get('django_timezone', 'UTC')
        timezone.activate(pytz.timezone(timezone_name))  # Активируем часовой пояс
        current_time = timezone.now()  # Получаем текущее время

        context['timezones'] = pytz.common_timezones  # Все доступные часовые пояса
        context['current_time'] = current_time  # Добавляем в контекст текущее время
            
        return context   


@login_required
def upgrade_user(request):
    user = request.user
    group = Group.objects.get(name='authors')
    if not user.groups.filter(name='authors').exists():
        group.user_set.add(user)
        Author.objects.get_or_create(authorUser=user)
    return redirect('news_list')


@login_required
def subscribe(request, pk):
    category = get_object_or_404(Category, id=pk)
    category.subscribers.add(request.user)
    message = _('You have successfully subscribed to category updates:')

    # Считываем выбранный часовой пояс из сессии
    timezone_name = request.session.get('django_timezone', 'UTC')
    user_timezone = pytz.timezone(timezone_name)
    current_time = timezone.now().astimezone(user_timezone)

    return render(request, 'subscribe.html', {
        'category': category,
        'message': message,
        'timezones': pytz.common_timezones,  # Все доступные часовые поясы
        'current_time': current_time  # Текущее время в выбранном поясе
    })


@login_required
def delete_subscribe(request, pk):
    category = get_object_or_404(Category, id=pk)
    category.subscribers.remove(request.user)
    message = _('You have successfully unsubscribed from updates in the category:')

    # Считываем выбранный часовой пояс из сессии
    timezone_name = request.session.get('django_timezone', 'UTC')
    user_timezone = pytz.timezone(timezone_name)
    current_time = timezone.now().astimezone(user_timezone)

    return render(request, 'delete_subscribe.html', {
        'category': category,
        'message': message,
        'timezones': pytz.common_timezones,  # Все доступные часовые поясы
        'current_time': current_time  # Текущее время в выбранном поясе
    })


class CategoryList(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news'
    paginate_by = 10

    def get_queryset(self):
        self.post_category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(post_category=self.post_category).order_by('-date_creation')
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Считываем выбранный часовой пояс из сессии
        timezone_name = self.request.session.get('django_timezone', 'UTC')
        timezone.activate(pytz.timezone(timezone_name))  # Активируем часовой пояс
        current_time = timezone.now()  # Получаем текущее время

        context.update({
            'category': self.post_category,
            'filterset': self.filterset,
            'is_not_subscriber': user.is_authenticated and user not in self.post_category.subscribers.all(),
            'is_author': user.is_authenticated and user.groups.filter(name='authors').exists(),
            'timezones': pytz.common_timezones,  # Все доступные часовые пояса
            'current_time': current_time  # Добавляем текущее время в контекст
        })
        return context


class NewsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(publication='NW')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["post_category", "author",]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user, publication='NW')

    def perform_update(self, serializer):
        serializer.save(author=self.request.user, publication='NW')


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(publication='AR')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["post_category", "author",]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, publication='AR')

    def perform_update(self, serializer):
        serializer.save(author=self.request.user, publication='AR')
