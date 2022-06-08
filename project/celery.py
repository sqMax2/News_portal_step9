import os
from celery import Celery
from celery.schedules import crontab

# Event mode runs with gevent on Win:
# celery -A project worker -l info -P gevent

# Celery beat run on Win (but does nothing):
# python.exe -m celery -A project beat --loglevel=info

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# scheduled task
app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'newsapp.tasks.mail',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        # 'args': (),
    },
}
