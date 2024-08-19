import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery('config')
app.config_from_object('django.conf:settings', namespace = "CELERY")
app.conf.beat_schedule = {
    'network_traffic_handler_task':{
        'task':'traffic_analysis.api.tasks.network_traffic_handler_task',
        'schedule': 0.5 
    },
}
app.autodiscover_tasks()