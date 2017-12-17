#!/usr/bin/env python
# -*- coding: utf-8 -*-
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Field, Fieldset, Layout, Submit
from django import forms
from django.utils import timezone
from django_markdown.widgets import MarkdownWidget
from taggit_selectize.widgets import TagSelectize

from blog.models import Post


class PostForm(forms.ModelForm):
    publish = forms.BooleanField(initial=False, required=False)

    class Meta:
        fields = ('title', 'body', 'is_commentable', 'tags', 'published')
        widgets = {
            'tags': TagSelectize(),
            'body': MarkdownWidget,
        }
        model = Post

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        fields = [
            'title', 'body', 'is_commentable', 'tags', 'publish'
        ]
        if self.initial.get('publish'):
            # noinspection PyTypeChecker
            fields.insert(-1, Field('published', disabled=True))
        self.helper.layout = Layout(
            Fieldset(
                None,
                *fields
            ),
            FormActions(
                Submit('save', 'Submit'),
                HTML('<a href="{% url \'blog:list\' %}{% query_builder request %}">Go Back</a>')
            )
        )

    def save(self, commit=True):
        self.instance.published = timezone.now() if self.cleaned_data['publish'] else None
        return super(PostForm, self).save(commit)
