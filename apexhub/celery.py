import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apexhub.settings")

celery = Celery("apexhub")

celery.config_from_object("django.conf:settings", namespace="CELERY")
celery.autodiscover_tasks()
