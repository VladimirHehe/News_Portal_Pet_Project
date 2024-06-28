import logging
from datetime import datetime, timedelta

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from news.models import Post, Category, Subscription
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.timezone import now

logger = logging.getLogger(__name__)


def send_mail_week():
    categories = Category.objects.filter(subscription__isnull=False).distinct()

    for category in categories:
        new_posts = Post.objects.filter(category=category, date_created__gte=datetime.now() - timedelta(days=7))
        subscriptions = Subscription.objects.filter(category=category)
        subscribers = [subscription.user for subscription in subscriptions]

        subject = f"Привет, в твоей любимой категории есть несколько обновлений!"
        text_content = render_to_string("weekly_digest.txt", {"new_posts": new_posts, "category": category})
        html_content = render_to_string("weekly_digest.html", {"new_posts": new_posts, "category": category})

        for subscriber in subscribers:
            msg = EmailMultiAlternatives(subject, text_content, 'sobetskyvladimir@yandex.ru', [subscriber.email])
            msg.attach_alternative(html_content, "text/html")
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

        scheduler.add_job(
            send_mail_week,
            trigger=CronTrigger(week="1"),
            id="send_mail_week",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'send_mail_week'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
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
