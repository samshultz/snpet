# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-07 14:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0004_auto_20171107_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippet',
            name='slug',
            field=models.SlugField(blank=True, unique_for_date='created'),
        ),
    ]
