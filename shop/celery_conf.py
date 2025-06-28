import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')
celery_app = Celery('shop')

celery_app.config_from_object("django.conf:settings",namespace="CELERY")
celery_app.autodiscover_tasks()
celery_app.conf.worker_prefetch_multiplier = 4 #هر ورکری حق داره چندتا تسک رو همزمان انجام بده - چون تسک های ما سبکه میزاریم 4