from django.utils.translation import gettext_lazy as _
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime, timedelta

from .models import PostCategory, Post, Category


@shared_task
def send_notifications(preview, pk, title, subscribers, category):
    for email, first_name in subscribers:
        html_content = render_to_string(
            'new_created_email.html',
            {
                'name': first_name,
                'category': category,
                'title': title,
                'text': preview,
                'link': f'{settings.SITE_URL}/news/{pk}',
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'New publication in category "{category}"',
            body='', 
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def notify_weekly():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(date_creation__gte=last_week)
    categories = set(posts.values_list('post_category__name_category', flat=True))
    subscribers = set(Category.objects.filter(name_category__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='All publications for the past week',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=list(subscribers),
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()