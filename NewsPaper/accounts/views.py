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


# class SignUp(CreateView):
#     model = User
#     form_class = BasicSignupForm
#     success_url = reverse_lazy('news_list')

#     template_name = 'registration/signup.html'

#     def form_valid(self, form):
#             response = super().form_valid(form)
            
#             # Добавляем пользователя в группу common сразу после сохранения
#             common_group, created = Group.objects.get_or_create(name='common')
#             self.object.groups.add(common_group)

#             return response


# class LoginUserView(LoginView):
#     form_class = AuthenticationForm
#     template_name = 'registration/login.html'

#     def get_success_url(self):
#         return reverse_lazy('news_list')
    

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