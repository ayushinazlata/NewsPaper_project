from django.urls import path
from .views import (ProfileEdit, LoginUserView, logout_user)


app_name = 'accounts'

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/edit/', ProfileEdit.as_view(), name='profile_edit'),
]