# pylint: disable=C0103
# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-10 21:06
from __future__ import unicode_literals

from django.db import migrations

import taggit_selectize.managers


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_auto_20170809_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=taggit_selectize.managers.TaggableManager(
                blank=True,
                help_text='A comma-separated list of tags.',
                through='taggit.TaggedItem',
                to='taggit.Tag',
                verbose_name='Tags'),
        ),
    ]
