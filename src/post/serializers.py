#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy

from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import get_error_detail
from rest_framework.relations import PrimaryKeyRelatedField

from post.models import Post


class PostSerializer(serializers.ModelSerializer):
    """
        Serializer for retrieving or modifying an existing post
    """

    class Meta:
        model = Post
        # TODO: Add `tags` field to serializer
        fields = ('id', 'user', 'title', 'published', 'updated', 'body', 'created')
        read_only_fields = ('user', 'published')

    user = PrimaryKeyRelatedField(read_only=True, source='user.username')

    # Adds missing fields to `value` for partial update if these fields exists in validator and missing in `value`
    # I fixed it in PR https://github.com/encode/django-rest-framework/pull/5748
    def run_validators(self, value):
        errors = []
        for validator in self.validators:
            if hasattr(validator, 'set_context'):
                validator.set_context(self)

            value_ext = copy.copy(value)
            if getattr(self.root, 'partial', False):
                if hasattr(validator, 'date_field') and validator.date_field not in value_ext:
                    value_ext[validator.date_field] = \
                        self.fields.fields.get(validator.date_field).to_internal_value(
                            getattr(self.instance, validator.date_field))
                if hasattr(validator, 'field') and validator.field not in value_ext:
                    value_ext[validator.field] = \
                        self.fields.fields.get(validator.field).to_internal_value(
                            getattr(self.instance, validator.field))

            try:
                validator(value_ext)
            except ValidationError as exc:
                # If the validation error contains a mapping of fields to
                # errors then simply raise it immediately rather than
                # attempting to accumulate a list of errors.
                if isinstance(exc.detail, dict):
                    raise
                errors.extend(exc.detail)
            except DjangoValidationError as exc:
                errors.extend(get_error_detail(exc))
        if errors:
            raise ValidationError(errors)


class PublishFieldSerializer(serializers.BooleanField):
    def to_internal_value(self, data):
        return timezone.now() if data else None

    def to_representation(self, value):
        return value is not None


class CreatePostSerializer(serializers.ModelSerializer):
    """
        Serializer for creating a new post
    """

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'created', 'updated', 'published', 'body', 'publish')
        read_only_fields = ('user', 'published')

    publish = PublishFieldSerializer(source='published')
    user = PrimaryKeyRelatedField(read_only=True, source='user.username')
