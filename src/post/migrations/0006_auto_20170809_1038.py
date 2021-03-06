# pylint: disable=C0103
# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-09 07:38
from __future__ import unicode_literals

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0005_post_updated'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={
                'ordering': ('-posted', ),
                'verbose_name': 'blog post',
                'verbose_name_plural': 'blog posts'
            },
        ),
        migrations.RenameField(
            model_name='post',
            old_name='_body_rendered',
            new_name='_content_rendered',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='body',
            new_name='content',
        ),
        migrations.RemoveField(
            model_name='post',
            name='pubdate',
        ),
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='is_commentable',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='post',
            name='posted',
            field=models.DateTimeField(
                auto_now_add=True,
                db_index=True,
                default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=taggit.managers.TaggableManager(
                blank=True,
                help_text='A comma-separated list of tags.',
                through='taggit.TaggedItem',
                to='taggit.Tag',
                verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(
                default=1,
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=100, unique_for_date='posted'),
        ),
    ]
