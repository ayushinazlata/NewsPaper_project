from django.urls import path
from .views import NewsList, NewList


urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', NewList.as_view()),
]