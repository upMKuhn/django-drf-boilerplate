from datetime import datetime
from django.utils import timezone

from core.models import Settings


class SettingsService:

    def get_settings(self):
        settings = Settings.objects.first()
        if not settings:
            settings = Settings()
        return settings
