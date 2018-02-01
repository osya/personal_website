# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-06 13:26
from __future__ import unicode_literals

from django.db import migrations, models
import precise_bbcode.fields


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20170804_0044'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='_body_rendered',
            field=models.TextField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='body',
            field=precise_bbcode.fields.BBCodeTextField(no_rendered_field=True),
        ),
    ]