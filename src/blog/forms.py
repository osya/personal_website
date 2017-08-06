#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from .models import Post


class CommonFormHelper(FormHelper):
    def __init__(self):
        super(CommonFormHelper, self).__init__()
        self.disable_csrf = True
        self.form_tag = False


class PostForm(forms.ModelForm):
    class Meta:
        fields = ('title', 'body',)
        labels = {
            'title': '',
            'body': '',
        }
        model = Post

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.helper = CommonFormHelper()
        self.helper.layout = Layout(
                Field('title', readonly=True),
                Field('body', readonly=True),
        )
