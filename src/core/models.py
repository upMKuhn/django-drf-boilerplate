from datetime import datetime

import uuid
from django.db import models
from django.db.models import Count
from django.utils import timezone
from random import randint


class BaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_on = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    updated_on = models.DateTimeField(auto_now=True, editable=False, db_index=True)

    @classmethod
    def random(cls):
        count = cls.objects.aggregate(count=Count('id'))['count']
        if count == 0:
            return None
        random_index = randint(0, count - 1)
        return cls.objects.all()[random_index]

    @classmethod
    def get_or_none(cls, **kwargs):
        """
        Uses get() to return an object or None if the object does not exist.
        All other passed arguments and keyword arguments are used in the get() query.
        Note: Like with get(), a MultipleObjectsReturned will be raised if more than one
        object is found.
        """
        try:
            return cls.objects.get(**kwargs)
        except cls.objects.model.DoesNotExist:
            return None

    def to_dict(self):
        return {f: self.__dict__.get(f) for f in self.get_all_field_names(True)}

    def get_all_field_names(self, include_relations=True, include_meta_fields=False):
        """
        Get all non relation fields, maybe leaving out meta fields
        :param include_relations:
        :param include_meta_fields:
        :return:
        """
        meta_fields = ['id', 'updated_on', 'created_on'] if not include_meta_fields else []

        relation_filter = (lambda f: f.one_to_one or (f.many_to_one and f.related_model)
                           ) if include_relations else lambda f: False
        meta_field_filter = (lambda f: True) if include_meta_fields else lambda f: f.name not in meta_fields

        return [
            f.name
            for f in self.__class__._meta.get_fields()
            if relation_filter(f) or (not f.is_relation and meta_field_filter(f))
        ]

    class Meta:
        abstract = True


class Settings(BaseModel):
    dummy_setting = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Settings'

