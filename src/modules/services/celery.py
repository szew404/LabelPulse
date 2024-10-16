from __future__ import absolute_import, unicode_literals

from celery import Celery

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.config.settings")

app = Celery("services")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(["services"])


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
