from django.db import models
from django.contrib.auth.models import User
from djmoney.models.fields import MoneyField
from account.models import Checking_Account
from registration.models import TimeStampedModel


# transfer to other person
class LogExternal(TimeStampedModel):
    LOG_CHOICES = (
        ('T', 'Transfer'),
        ('D', 'Deposit'),
        ('W', 'Withdraw'),
    )
    type = models.CharField(max_length=1, choices=LOG_CHOICES, blank=False)
    amount = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='USD',
        max_digits=11,
    )
    account_1 = models.OneToOneField(Checking_Account, on_delete=models.CASCADE, related_name='external_account_1', blank=False, null=False)
    account_2 = models.OneToOneField(Checking_Account, on_delete=models.CASCADE, related_name='external_account_2', blank=True, null=True)

    def __unicode__(self):
        return 'LogExternal(id=' + str(self.id) + ')'


# transfer between own accounts
class LogInternal(TimeStampedModel):
    LOG_CHOICES = (
        ('C', 'toChecking'),
        ('S', 'toSaving'),
    )
    type = models.CharField(max_length=1, choices=LOG_CHOICES, blank=False)
    amount = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='USD',
        max_digits=11,
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='external_user', blank=False, null=False)

    def __unicode__(self):
        return 'LogInternal(id=' + str(self.id) + ')'
