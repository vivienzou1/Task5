from django.db import models
from django.contrib.auth.models import User
from djmoney.models.fields import MoneyField


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
    user_1 = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_1')
    account_1
    user_2 = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_2')
    account_2

    def __unicode__(self):
        return 'Log(id=' + str(self.id) + ')'
