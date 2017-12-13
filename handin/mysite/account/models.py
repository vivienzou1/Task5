from __future__ import unicode_literals
from djmoney.models.fields import MoneyField
from django.db import models
# User class for built-in authentication module
from django.contrib.auth.models import User
from registration.models import Profile

# Create your models here.

class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Account(TimeStampedModel):
    profile = models.OneToOneField(Profile, on_delete = models.CASCADE)
    account_number = models.BigIntegerField(unique=True)
    account_status = models.CharField(max_length= 100, default="active")


    def __str__(self):
        return 'id = ' + str(self.id) + " user = " + str(self.profile.user.username)

class Saving_Account(models.Model):
    balance = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='USD',
        max_digits=11,
    )
    account_number = models.BigIntegerField(unique=True)
    account = models.OneToOneField(Account,
                                   on_delete=models.CASCADE,
                                   unique=True,
                                   related_name="saving_account")
    def __unicode__(self):
        return str(self.account.profile.user.username) + "'s saving account"

class Checking_Account(models.Model):
    balance = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='USD',
        max_digits=11,
    )
    account_number = models.BigIntegerField(unique=True)
    account = models.OneToOneField(Account,
                                   on_delete=models.CASCADE,
                                   unique=True,
                                   related_name="checking_account")
    def __str__(self):
        return str(self.account.profile.user.username) + "'s check account"
