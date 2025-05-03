from django.urls import path, include
from .views import (ProfileEdit, logout_user)


app_name = 'accounts'

urlpatterns = [
    path('logout/', logout_user, name='logout'),
    path('profile/edit/', ProfileEdit.as_view(), name='profile_edit'),
    path('', include('allauth.urls')),
]