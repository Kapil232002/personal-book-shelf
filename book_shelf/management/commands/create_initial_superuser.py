from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = "Creates a superuser from environment variables if not already present."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not username or not email or not password:
            self.stdout.write(self.style.ERROR("❌ Missing one or more environment variables"))
            self.stdout.write(f"  USERNAME: {'✅' if username else '❌ MISSING'}")
            self.stdout.write(f"  EMAIL:    {'✅' if email else '❌ MISSING'}")
            self.stdout.write(f"  PASSWORD: {'✅' if password else '❌ MISSING'}")
            return

        User = get_user_model()
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS("✅ Superuser created!"))
        else:
            self.stdout.write("🟡 Superuser already exists.")
