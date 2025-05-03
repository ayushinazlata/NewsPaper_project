from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group, User
from django.utils.translation import gettext_lazy as _ 


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group, created = Group.objects.get_or_create(name='common') 
        basic_group.user_set.add(user)
        return user


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': _('Name'),
            'last_name': _('Last Name'),
            'email': _('Email'),
        }