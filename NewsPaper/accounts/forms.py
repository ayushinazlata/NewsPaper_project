from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group, User

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