from __future__ import unicode_literals

from django.apps import AppConfig


class TasksConfig(AppConfig):
    name = 'tasks'
    def ready(self):
        from tasks import signals