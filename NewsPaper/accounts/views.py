from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm

from .forms import BasicSignupForm, ProfileEditForm
from news.models import Author


class ProfileEdit(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = 'registration/profile_edit.html'
    success_url = reverse_lazy('news_list')

    def get_object(self, queryset=None):
        return self.request.user


def logout_user(request):
    logout(request)
    return redirect('news_list')