from django_filters import FilterSet, ModelChoiceFilter, DateFilter, CharFilter
from django.forms import DateInput
from .models import Post, Author, Category

class PostFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='По названию'
    )

    author = ModelChoiceFilter(
        field_name='author',
        queryset=Author.objects.all(),
        label='Автор',
        empty_label='Выберите автора'
    )

    date_creation_after = DateFilter(
        field_name='date_creation',
        lookup_expr='gte',
        label='Дата публикации после',
        widget=DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = []
