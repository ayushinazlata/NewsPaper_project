from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import NewsForm
from .models import Post, Author, Category
from .filters import PostFilter, UserNewsFilter
from django.shortcuts import redirect, render, get_object_or_404
from datetime import datetime, timedelta
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.decorators import login_required


class NewsList(ListView):
    model = Post
    ordering = '-date_creation'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        context['is_author'] = user.is_authenticated and user.groups.filter(name='authors').exists()
        context['date_creation'] = datetime.utcnow()

        if user.is_authenticated and context['is_author']:
            limit = settings.DAY_LIMIT_POSTS
            prev_day = timezone.now() - timedelta(hours=24)
            posts_day_count = Post.objects.filter(
                date_creation__gte=prev_day,
                author__authorUser=user
            ).count()

            context.update({
                'limit': limit,
                'count': posts_day_count,
                'posts_limit': posts_day_count >= limit,
            })
        else:
            context.update({'limit': 0, 'count': 0, 'posts_limit': False})

        return context


class NewList(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


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
        context['filterset'] = self.filterset
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


class NewsEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)  # исправил на корректное право
    form_class = NewsForm
    model = Post
    template_name = 'new_edit.html'
    success_url = reverse_lazy('user_news')


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'new_delete.html'
    success_url = reverse_lazy('news_list')


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
    message = 'Вы успешно подписались на обновления категории:'
    return render(request, 'subscribe.html', {'category': category, 'message': message})


@login_required
def delete_subscribe(request, pk):
    category = get_object_or_404(Category, id=pk)
    category.subscribers.remove(request.user)
    message = 'Вы успешно отписались от обновлений в категории:'
    return render(request, 'delete_subscribe.html', {'category': category, 'message': message})


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

        context.update({
            'category': self.post_category,
            'filterset': self.filterset,
            'is_not_subscriber': user.is_authenticated and user not in self.post_category.subscribers.all(),
            'is_author': user.is_authenticated and user.groups.filter(name='authors').exists(),
        })
        return context
