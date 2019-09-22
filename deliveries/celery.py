from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from commons.library import send_slack_message

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('nora')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def call_send_link_task(self, link, delivery_id):
    print('Call send link task')
    send_slack_message(link, delivery_id)
    print('finish send link task')
