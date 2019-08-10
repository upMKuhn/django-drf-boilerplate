from datetime import datetime
from django.utils import timezone

from core.models import Settings


class SettingsService:

    def get_settings(self):
        settings = Settings.objects.first()
        if not settings:
            settings = Settings()
        return settings

    def update_last_company_sync(self, updated_at=None):
        settings = self.get_settings()
        settings.last_company_sync = updated_at or timezone.now()
        settings.save()

    def get_last_company_sync(self):
        settings = self.get_settings()
        return settings.last_company_sync if settings else None

    def update_last_complete_company_detail_sync(self, updated_at=None):
        settings = self.get_settings()
        settings.last_complete_company_detail_sync = updated_at or timezone.now()
        settings.save()

    def get_last_complete_company_detail_sync(self):
        settings = self.get_settings()
        return settings.last_complete_company_detail_sync if settings else None
