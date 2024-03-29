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
    period = models.IntegerField(
        blank=False,
        null=False)
    interest = models.DecimalField(
        decimal_places=5,
        max_digits=10,
        blank=False,
        null=False)

    def __str__(self):
        return 'Loan(' + 'type=' + str(self.type) + " "\
               + 'amount=' + str(self.amount) + " "\
               + 'period=' + str(self.period) + ")"


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
    interest = models.DecimalField(
        decimal_places=5,
        max_digits=10,
        blank=False,
        null=False)

    def __unicode__(self):
        return 'LoanLog(id=' + str(self.id) + ')'
