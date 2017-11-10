from django.db import models
from django.contrib.auth.models import User
from djmoney.models.fields import MoneyField
from account.models import Checking_Account


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Log(TimeStampedModel):
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
    account_1 = models.OneToOneField(Checking_Account, on_delete=models.CASCADE, related_name='account_1', blank=False, null=False)
    account_2 = models.OneToOneField(Checking_Account, on_delete=models.CASCADE, related_name='account_2', blank=True, null=True)

    def __unicode__(self):
        return 'Log(id=' + str(self.id) + ')'
