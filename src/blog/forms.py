#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit
from taggit_selectize.widgets import TagSelectize

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        fields = ('title', 'description', 'content', 'is_commentable', 'tags',)
        widgets = {'tags': TagSelectize(), }
        model = Post

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
                'title', 'description', 'content', 'is_commentable', 'tags',
                ButtonHolder(
                        Submit('submit', 'Submit', css_class='btn btn-default')
                )
        )
