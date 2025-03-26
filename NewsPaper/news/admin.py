from django.contrib import admin
from .models import Author, Category, Post, Comment, PostCategory


def nullfy_rating(modeladmin, request, queryset):
    queryset.update(rating=0)
    nullfy_rating.short_description = 'Reset rating'


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'publication', 'title', 'date_creation', 'rating')
    list_filter = ('author', 'publication', 'date_creation')
    search_fields = ('author', 'publication', 'title', 'date_creation', 'rating')
    actions = [nullfy_rating]


class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_post', 'comment_user', 'text', 'date_creation', 'rating')
    list_filter = ('comment_user', 'date_creation')
    search_fields = ('comment_post', 'comment_user', 'text', 'rating')
    actions = [nullfy_rating]


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment, CommentAdmin)

