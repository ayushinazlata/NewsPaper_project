from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from .forms import NewsForm
from .models import Post, Author
from .filters import PostFilter
from datetime import datetime
from django.urls import reverse_lazy


class NewsList(ListView):
    model = Post
    ordering = '-date_creation'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_creation'] = datetime.utcnow()
        return context


class NewList(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


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


class NewsCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'new_edit.html'

    def form_valid(self, form):
        user = self.request.user
        
        # Проверяем, есть ли у пользователя связанный Author
        if not hasattr(user, 'author'):
            # Если нет - создаём его автоматически
            author = Author.objects.create(authorUser=user)
        else:
            author = user.author

        post = form.save(commit=False)
        post.author = author  # Присваиваем созданного/существующего автора
        return super().form_valid(form)


class NewsEdit(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'new_edit.html'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'new_delete.html'
    success_url = reverse_lazy('news_list')