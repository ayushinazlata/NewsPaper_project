from django.views.generic import ListView, DetailView
from .models import Post
from datetime import datetime


class NewsList(ListView):
    model = Post
    ordering = '-date_creation'
    template_name = 'news.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_creation'] = datetime.utcnow()
        return context


class NewList(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'