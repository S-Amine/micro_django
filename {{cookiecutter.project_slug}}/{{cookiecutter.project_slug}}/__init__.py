from __future__ import absolute_import, unicode_literals
from .celery import app as celery_app

# Make it possible to import the Celery application via the celery_app variable
__all__ = ('celery_app',)
