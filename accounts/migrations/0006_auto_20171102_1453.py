# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-02 13:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20171102_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='website',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
