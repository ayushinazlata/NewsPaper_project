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
        queryset=Author.objects.filter(post__isnull=False).distinct(),
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



class UserNewsFilter(FilterSet):
    category = ModelChoiceFilter(
        field_name='post_category',
        queryset=Category.objects.all(),
        label=('Категория'),
        empty_label=('выберите категорию'),
    )

    date_creation_after = DateFilter(
        field_name='date_creation',
        label=('Публикации от'),
        lookup_expr='gt',
        widget=DateInput(
            format='%Y-%m-%dT',
            attrs={'type': 'date'},
        ),
    )
