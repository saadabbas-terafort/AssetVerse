import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create the initial staff superuser from ADMIN_EMAIL and ADMIN_PASSWORD."

    def handle(self, *args, **options):
        email = os.getenv("ADMIN_EMAIL", "").strip()
        password = os.getenv("ADMIN_PASSWORD", "")
        if not email or not password:
            self.stdout.write("ADMIN_EMAIL and ADMIN_PASSWORD are not both set; no user created.")
            return

        user_model = get_user_model()
        if user_model.objects.filter(email__iexact=email).exists():
            self.stdout.write(f"A user with {email} already exists; no user created.")
            return

        user_model.objects.create_superuser(email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Created superuser {email}."))
