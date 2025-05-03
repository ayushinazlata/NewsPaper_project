from django.core.cache import cache
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author')
    authorRating = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = postRat.get('postRating') or 0

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = commentRat.get('commentRating') or 0

        self.authorRating = (pRat * 3) + cRat
        self.save()

    def __str__(self):
        return f'{self.authorUser}'

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')


class Category(models.Model):
    name_category = models.CharField(
        max_length=64,
        unique=True,
        help_text=_('name category'),
        verbose_name=_('Category Name'),
    )
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return f'{self.name_category}'

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Post(models.Model):
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        help_text=_('Author of publication'),
        verbose_name=_('Author'),
    )

    ARTICLE = 'AR'
    NEWS = 'NW'
    CATEGORIES = (
        (NEWS, _('News')),
        (ARTICLE, _('Article')),
    )

    publication = models.CharField(
        max_length=2,
        choices=CATEGORIES,
        default=NEWS,
        verbose_name = _('Publication'),
    )
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name=_('Date of publication'))
    post_category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=256, verbose_name=_('Title'))
    text = models.TextField(verbose_name=_('Text'))
    rating = models.SmallIntegerField(default=0, verbose_name=_('Rating'))

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:124] + '...'

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')

    def delete(self, *args, **kwargs):
        cache.delete(f'post-{self.pk}')
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = _('Publication')
        verbose_name_plural = _('Publications')


class PostCategory(models.Model):
    post_through = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_through = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post_through}'

    class Meta:
        verbose_name = _('Post Category')
        verbose_name_plural = _('Post Categories')



class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.comment_post}'

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
