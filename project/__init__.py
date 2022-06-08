from .celery import app as celery_app

# initializing Celery
__all__ = ('celery_app',)