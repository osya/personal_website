# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-17 21:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('blog', '0012_post_published'), ('blog', '0013_remove_post_publish'), ('blog', '0014_auto_20171214_1616'), ('blog', '0015_remove_post_description')]

    dependencies = [
        ('blog', '0011_auto_20170821_1705'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='published',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='post',
            name='publish',
        ),
        migrations.RemoveField(
            model_name='post',
            name='description',
        ),
    ]