from .models import Category, Post, PostCategory
from modeltranslation.translator import register, TranslationOptions


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name_category',) 


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = (
        'title',
        'text',
    ) 