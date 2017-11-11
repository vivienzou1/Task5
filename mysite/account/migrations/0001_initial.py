# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-11 04:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('account_number', models.BigIntegerField(unique=True)),
                ('account_status', models.CharField(default='active', max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Checking_Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.PositiveIntegerField(default=0)),
                ('account_number', models.BigIntegerField(unique=True)),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='checking_account', to='account.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Saving_Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.PositiveIntegerField(default=0)),
                ('account_number', models.BigIntegerField(unique=True)),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='saving_account', to='account.Account')),
            ],
        ),
    ]
