#!/usr/bin/env python
# -*- coding: utf-8 -*-
from crispy_forms.bootstrap import FieldWithButtons, FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Field, Fieldset, Layout, Submit
from django import forms
from django.urls import reverse
from django.utils import timezone
from django_markdown.widgets import MarkdownWidget
from taggit_selectize.widgets import TagSelectize

from post.models import Post


class SearchForm(forms.Form):
    query = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_action = reverse('post:list')
        self.helper.form_class = 'navbar-form navbar-left'
        self.helper.attrs = {'role': 'search'}
        self.helper.form_method = 'GET'
        self.helper.layout = Layout(
            FieldWithButtons(
                Field('query', autofocus='autofocus'),
                Submit('', 'Search')
            )
        )


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
                HTML('<a href="{% url \'post:list\' %}{% query_builder request %}">Go Back</a>')
            )
        )

    def save(self, commit=True):
        if self.cleaned_data.get('publish'):
            if self.cleaned_data.get('published') is None:
                self.instance.published = timezone.now()
            self.cleaned_data.pop('publish')
        return super(PostForm, self).save(commit)
