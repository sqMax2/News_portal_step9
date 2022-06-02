# runapscheduler.py
import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
#sending mails
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth.models import User
import datetime
from project.settings import DEFAULT_FROM_EMAIL
# newsapp
from newsapp.models import Category, Post


logger = logging.getLogger(__name__)


def my_job():
    # Your job processing logic here...
    weekEarlier = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc) - datetime.timedelta(days=7)

    for u in User.objects.all():
        categoryList = list(u.categories.all().values_list('name', flat=True))
        if len(categoryList):
            qs = Post.objects.filter(dateCreation__gt=weekEarlier).filter(postCategory__in=u.categories.all())
            subject = f'Your weekly news:{", ".join(categoryList)} since {weekEarlier.strftime("%d.%m.%Y")}'
            body = f'News are: {". ".join(list(qs.values_list("title", flat=True)))}'
            # categoryType = dict(qs.CATEGORY_CHOICES)[qs.categoryType]
            # redirectURL = f'/{categoryType.lower()}{"s" if categoryType[-1] != "s" else ""}/{qs.id}'
            html_content = render_to_string(
                'weekly_mail.html',
                {
                    'news_list': qs,
                    'user': u,
                    'subject': subject
                }
            )
            # mailing list
            mailing_list = [u.email]
            if len(mailing_list):
                msg = EmailMultiAlternatives(
                    subject=subject,
                    body=body,
                    from_email=DEFAULT_FROM_EMAIL,
                    to=mailing_list
                )
                msg.attach_alternative(html_content, 'text/html')
                msg.send()


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            #trigger=CronTrigger(day_of_week='sun'),  # fires trigger every sunday
            trigger=CronTrigger(second="*/10"),  # Every 10 seconds
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
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
