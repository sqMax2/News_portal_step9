from celery import shared_task
import time
# mailing
from django.core.mail import EmailMultiAlternatives
from project.settings import DEFAULT_FROM_EMAIL
from newsapp.models import Category, Post
from django.contrib.auth.models import User
from django.template.loader import render_to_string
import datetime


@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")


@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)


# mailing task. Same as in apscheduler
@shared_task
def mail():
    print('mailing task')
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
