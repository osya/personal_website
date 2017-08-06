#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    """
        This form currently not used. But probably will be used for creating new posts
    """
    class Meta:
        fields = ('title', 'body',)
        labels = {
            'title': '',
            'body': '',
        }
        model = Post
