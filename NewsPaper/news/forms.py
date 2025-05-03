from django import forms
from django.core.exceptions import ValidationError
from .models import Post
from django.utils.translation import gettext_lazy as _


class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['publication', 'title', 'text', 'post_category']

        labels = {
            'publication': _('Type of publication'),
            'title': _('Title'),
            'text': _('Text'),
            'post_category': _('Category'),
        }

        widgets = {
            'post_category': forms.CheckboxSelectMultiple(),
        }

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if title and title[0].islower():
            raise ValidationError(_("The name must start with a capital letter"))
        return title
