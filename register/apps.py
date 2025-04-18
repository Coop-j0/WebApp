from django.apps import AppConfig
from django.db.models.signals import post_migrate

from payapp.apps import create_default_admin

class RegisterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'register'

class PayappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payapp'

    def ready(self):
        post_migrate.connect(create_default_admin, sender=self)