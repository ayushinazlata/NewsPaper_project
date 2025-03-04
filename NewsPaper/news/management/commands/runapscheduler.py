import logging
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from datetime import datetime, timedelta

from news.models import Post, Category

logger = logging.getLogger(__name__)

# наша задача по отправке писем
def my_job():
    today = datetime.now()
    last_week = today - timedelta(days=7)

    # Получаем все категории
    categories = Category.objects.all()

    # Для каждой категории находим подписчиков и отправляем им письмо
    for category in categories:
        # Посты, которые были созданы за последнюю неделю и относятся к этой категории
        posts = Post.objects.filter(
            date_creation__gte=last_week,
            post_category=category
        )

        # Подписчики этой категории
        subscribers = category.subscribers.all()

        # Если есть новые посты для подписчиков
        if posts.exists():
            for subscriber in subscribers:
                html_content = render_to_string(
                    'daily_post.html',
                    {
                        'link': settings.SITE_URL,
                        'posts': posts,
                        'name': subscriber.first_name or subscriber.username,
                        'category': category.name_category,
                    }
                )

                msg = EmailMultiAlternatives(
                    subject=f'Новые статьи в категории: {category.name_category}',
                    body='',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[subscriber.email],
                )
                msg.attach_alternative(html_content, 'text/html')
                msg.send()

# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="01", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
