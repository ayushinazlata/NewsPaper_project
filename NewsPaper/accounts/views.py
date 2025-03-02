from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import ProfileEditForm
from django.shortcuts import redirect
from news.models import Author
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout


class LoginUserView(LoginView):
    form_class = AuthenticationForm
    template_name = 'registration/login.html'
    

class ProfileEdit(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = 'registration/profile_edit.html'
    success_url = reverse_lazy('news_list')

    def get_object(self, queryset=None):
        return self.request.user


def logout_user(request):
    logout(request)
    return redirect('/news')