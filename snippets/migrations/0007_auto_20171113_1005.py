# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-13 09:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0006_auto_20171108_2017'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='snippet',
            options={'ordering': ('-created',)},
        ),
    ]
