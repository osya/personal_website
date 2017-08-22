#!/usr/bin/env python
# -*- coding: utf-8 -*-
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit
from django import forms
from django_markdown.widgets import MarkdownWidget
from taggit_selectize.widgets import TagSelectize

from blog.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        fields = ('title', 'description', "body", 'is_commentable', 'tags',)
        widgets = {
            'tags': TagSelectize(),
            'body': MarkdownWidget,
        }
        model = Post

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
                'title', 'description', 'body', 'is_commentable', 'tags',
                ButtonHolder(
                        Submit('submit', 'Submit', css_class='btn btn-default')
                )
        )
