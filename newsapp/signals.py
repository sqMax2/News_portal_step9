# signal
from .models import Author, Category, Post, Comment, PostCategory
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.db import transaction
from project.settings import DEFAULT_FROM_EMAIL


def on_transaction_commit(func):
    def inner(*args, **kwargs):
        transaction.on_commit(lambda: func(*args, **kwargs))

    return inner


@receiver(m2m_changed, sender=PostCategory)
# @on_transaction_commit
def notify_subscribers(sender, instance, action, **kwargs):
    # print(instance)
    if action == 'post_add':
        categoryType = dict(instance.CATEGORY_CHOICES)[instance.categoryType]
        redirectURL = f'/{categoryType.lower()}{"s" if categoryType[-1]!="s" else ""}/{instance.id}'
        html_content = render_to_string(
            'post_created_mail.html',
            {
                'post': instance,
                'redirectURL': redirectURL,
            }
        )
        # mailing list
        mailing_list = list(set(instance.postCategory.all().values_list('subscribers__email', flat=True)))
        if '' in mailing_list:
            mailing_list.remove('')
        # print(action)
        # print(instance.postCategory)
        if len(mailing_list):
            msg = EmailMultiAlternatives(
                subject=f'{instance.author.authorUser.username}: {instance.title} '
                        f'{instance.dateCreation.strftime("%d.%m.%Y")}',
                body=instance.text,
                from_email=DEFAULT_FROM_EMAIL,
                to=mailing_list
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()

# post_save.connect(notify_subscribers, sender=Post)