# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-13 02:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_auto_20171213_0129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='middle_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
