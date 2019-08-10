from django.core.files import File
from django.db import models

import hashlib
from core.models import BaseModel


def hash_file(file: File) -> str:
    hasher = hashlib.sha256()
    for chunk in file.chunks():
        hasher.update(to_bytes(chunk))
    return hasher.hexdigest()


def to_bytes(content):
    if isinstance(content, str):
        return content.encode()
    return bytes(content)


def content_file_name(instance, filename):
    filename = hash_file(instance.video)
    return '/'.join(['uploads', instance.video.name + '_' + filename])


class AlertVideo(BaseModel):
    video = models.FileField(upload_to=content_file_name)
    name = models.CharField(max_length=255, blank=False, null=False)
    hash = models.CharField(max_length=255, blank=False, null=False)

    def save(self, **kwargs):
        self.clean()
        super().save(**kwargs)

    def clean(self):
        if self._state.adding:
            self.name = self.video.name
            self.hash = hash_file(self.video)
        super().clean()

    class Meta:
        verbose_name_plural = 'Alert Events'
