# pylint: disable=C0103
# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-21 12:45
from __future__ import unicode_literals

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0008_auto_20170821_1531'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={
                'ordering': ('-created', ),
                'verbose_name': 'Blog Post',
                'verbose_name_plural': 'Blog Posts'
            },
        ),
        migrations.RenameField(
            model_name='post',
            old_name='posted',
            new_name='created',
        ),
        migrations.AddField(
            model_name='post',
            name='publish',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=100, unique_for_date='created'),
        ),
    ]
