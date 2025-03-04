from django.urls import path, include
from .views import (ProfileEdit, logout_user)


app_name = 'accounts'

urlpatterns = [
    # path('signup/', SignUp.as_view(), name='signup'),
    # path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/edit/', ProfileEdit.as_view(), name='profile_edit'),
    path('', include('allauth.urls')),
]