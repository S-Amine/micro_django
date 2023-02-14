import os
from celery import Celery

# Set the default Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{cookiecutter.project_slug}}.settings')

# Create an instance of the Celery app
app = Celery('{{cookiecutter.project_slug}}')

# Load the configuration data from django.conf.settings
# All configuration keys should have a `CELERY_` prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps
app.autodiscover_tasks()

# Create a task that prints out the request object
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
