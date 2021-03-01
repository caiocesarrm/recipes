from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from kombu import Queue, Exchange
# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
os.environ.setdefault('C_FORCE_ROOT', 'true')
current_env = os.environ.get('CURRENT_ENV')

app = Celery("abrecipes")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

default_exchange = Exchange('abrecipes')

app.conf.task_queues = (
    Queue(f'email_{current_env}', default_exchange, routing_key='email', queue_arguments={'x-max-priority': 15}),
    Queue(f'image_processing{current_env}', default_exchange, routing_key='image_processing', queue_arguments={'x-max-priority': 15}),
)

#app.conf.task_default_queue = 'default'
#app.conf.task_default_exchange = f'default_{current_env}'
#app.conf.task_default_routing_key = 'default'

app.conf.update(
    worker_prefetch_multiplier=20,
    task_acks_late=True,
    worker_max_tasks_per_child=40
)

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))