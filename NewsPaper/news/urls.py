from django.urls import path
from .views import (NewsList, NewList, NewsSearch, NewsCreate, NewsEdit, NewsDelete)


urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', NewList.as_view()),
    path('', NewsList.as_view(), name='news_list'),
    path('<int:pk>', NewList.as_view(), name='new_detail'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit', NewsEdit.as_view(), name='new_edit'),
    path('<int:pk>/delete', NewsDelete.as_view(), name='new_delete'),
]