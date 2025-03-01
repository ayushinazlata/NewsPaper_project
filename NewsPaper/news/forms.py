from django import forms
from django.core.exceptions import ValidationError
from .models import Post

class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['publication', 'title', 'text', 'post_category']

        labels = {
            'publication': 'Тип публикации',
            'title': 'Заголовок',
            'text': 'Текст',
            'post_category': 'Категория',
        }

        widgets = {
            'post_category': forms.CheckboxSelectMultiple(),
        }

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if title and title[0].islower():
            raise ValidationError("Название должно начинаться с заглавной буквы")
        return title
