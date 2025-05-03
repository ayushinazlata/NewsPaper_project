from django.contrib import admin
from .models import Author, Category, Post, Comment, PostCategory
from modeltranslation.admin import TranslationAdmin
from django.utils.translation import gettext_lazy as _


def nullfy_rating(modeladmin, request, queryset):
    queryset.update(rating=0)
nullfy_rating.short_description = _('Reset rating')


class PostAdmin(TranslationAdmin, admin.ModelAdmin):
    list_display = ('author', 'publication', 'title', 'date_creation', 'rating')
    list_filter = ('author', 'publication', 'date_creation')
    search_fields = ('author__user__username', 'title', 'text')
    actions = [nullfy_rating]


class CategoryAdmin(TranslationAdmin, admin.ModelAdmin):
    list_display = ('name_category',)
    search_fields = ('name_category',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_post', 'comment_user', 'text', 'date_creation', 'rating')
    list_filter = ('comment_user', 'date_creation')
    search_fields = ('comment_post__title', 'comment_user__username', 'text', 'rating')
    actions = [nullfy_rating]


admin.site.register(Author)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment, CommentAdmin)
