# muiv_graduation_system/apps.py

from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class MuivGraduationSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'muiv_graduation_system'
    verbose_name = 'Платформа'

    def ready(self):
        from . import signals  # подключаем сигналы
        post_migrate.connect(signals.init_demo_data, sender=self)