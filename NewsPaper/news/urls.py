from django.urls import path
from .views import (NewsList, NewList, NewsSearch, NewsCreate, NewsEdit, NewsDelete, UserNewsListView, upgrade_user,
                    CategoryList, subscribe, delete_subscribe)
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', cache_page(60)(NewsList.as_view()), name='news_list'),
    path('<int:pk>/', cache_page(60 * 5)(NewList.as_view()), name='new_detail'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsEdit.as_view(), name='new_edit'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='new_delete'),
    path('my_news/', UserNewsListView.as_view(), name='user_news'),
    path('upgrade/', upgrade_user, name='upgrade_user'),
    path('categories/<int:pk>/', CategoryList.as_view(), name='category_news'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('categories/<int:pk>/unsubscribe', delete_subscribe, name='delete_subscribe'),  
]