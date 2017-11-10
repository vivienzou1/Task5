from __future__ import unicode_literals

from django.db import models
# User class for built-in authentication module
from django.contrib.auth.models import User

# Create your models here.

class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Account(TimeStampedModel):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    account_number = models.BigIntegerField(unique=True)
    account_status = models.CharField(max_length= 100, default="active")


    def __unicode__(self):
        return 'id = ' + self.id + " user = " + self.user

class Saving_Account(models.Model):
    balance = models.PositiveIntegerField(default = 0)
    account_number = models.BigIntegerField(unique=True)
    account = models.OneToOneField(Account,
                                   on_delete=models.CASCADE,
                                   unique=True,
                                   related_name="saving_account")

class Checking_Account(models.Model):
    balance = models.PositiveIntegerField(default = 0)
    account_number = models.BigIntegerField(unique=True)
    account = models.OneToOneField(Account,
                                   on_delete=models.CASCADE,
                                   unique=True,
                                   related_name="checking_account")
