import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car.settings')

app = Celery('car')

app.config_from_object('django.conf:settings', namespace = 'CELERY')
app.autodiscover_tasks()

# app.conf.beat_schedule={
#     'fetch-vk-clips-every-24-hours':{
#         'task': 'carapp.tasks.VK_clips',
#         'schedule': crontab(minute =  0, hour = 0),
#     },
#     'fetch-yandex-every-24-hours':{
#         'task': 'carapp.tasks.Yandex',
#         'schedule': crontab(minute =  0, hour = 0),
#     },
# }
