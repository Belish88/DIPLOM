from django.core.management import BaseCommand

from app_auth.models import Auth


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = Auth.objects.create(
            phone='0123456789',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('5080')
        user.save()
