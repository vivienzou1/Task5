from django.db import models
from djmoney.models.fields import MoneyField
from registration.models import TimeStampedModel
from registration.models import Profile


class Loan(TimeStampedModel):
    profile = models.ForeignKey(
        Profile,
        related_name='loan_profile',
        blank=False,
        null=False
    )
    LOAN_CHOICES = (
        ('A', 'Auto'),
        ('M', 'Mortgage'),
    )
    type = models.CharField(
        max_length=1,
        choices=LOAN_CHOICES,
        blank=False,
        null=False
    )
    amount = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='USD',
        max_digits=11,
    )
    cur_amount = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='USD',
        max_digits=11,
    )
    period = models.TimeField(max_length=20, blank=False, null=False)
    interest = models.DecimalField(max_length=20, blank=False, null=False)

    def __unicode__(self):
        return 'Loan(id=' + str(self.id) + ')'


class LoanLog(TimeStampedModel):
    loan = models.ForeignKey(
        Loan,
        related_name='log_loan',
        blank=False,
        null=False
    )
    amount = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='USD',
        max_digits=11,
    )
    interest = models.DecimalField(max_length=20, blank=False, null=False)

    def __unicode__(self):
        return 'LoanLog(id=' + str(self.id) + ')'
