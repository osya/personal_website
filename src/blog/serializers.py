#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework import serializers

from blog.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title',)
