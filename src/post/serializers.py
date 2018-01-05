#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework import serializers

from post.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'created', 'published', 'updated', 'body', 'tags')
