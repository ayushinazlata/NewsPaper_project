from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import PostCategory
from .tasks import send_notifications


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        for category in instance.post_category.all():
            subscribers = [(s.email, s.first_name or s.username) for s in category.subscribers.all()]
            send_notifications.apply_async(
                    (instance.preview(), instance.pk, instance.title, subscribers, category.name_category),
                    countdown=10
            )

