# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-11 19:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0003_logexternal_account_1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logexternal',
            name='account_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='external_account_1', to='account.Checking_Account'),
        ),
    ]