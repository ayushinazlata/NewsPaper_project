from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from .forms import NewsForm
from .models import Post, Author
from .filters import PostFilter, UserNewsFilter
from django.shortcuts import redirect
from datetime import datetime
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


class NewsList(ListView):
    model = Post
    ordering = '-date_creation'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_creation'] = datetime.utcnow()
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
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
        queryset = Post.objects.filter(author=self.request.user.author).order_by('-date_creation')
        self.filterset = UserNewsFilter(self.request.GET, queryset)
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
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = NewsForm
    model = Post
    template_name = 'new_edit.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        try:
            author = Author.objects.get(authorUser=self.request.user)
        except Author.DoesNotExist:
            # Если Author не найден, можно создать его или вернуть ошибку
            author = Author.objects.create(authorUser=self.request.user)

        self.object.author = author
        return super().form_valid(form)
    

class NewsEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.edit_post',)
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
        if not hasattr(user, 'author'):
            Author.objects.create(authorUser=user)
    return redirect('news_list')