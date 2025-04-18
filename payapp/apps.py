from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model

class RegisterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'register'

def create_default_admin(sender, **kwargs):
    User = get_user_model()
    if not User.objects.filter(username='admin1').exists():
        User.objects.create_superuser(
            username='admin1',
            email='admin1@example.com',
            password='admin1',
            first_name='Default',
            last_name='Admin'
        )
        print("Default admin user created (username: admin1, password: admin1)")

class PayappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payapp'

    def ready(self):
        import payapp.signals