from django import forms
from models import *


class AutoLoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['amount',
                  'period']

    def clean(self):
        cleaned_data = super(AutoLoanForm, self).clean()
        return cleaned_data


class MortgageLoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['amount',
                  'period']

    def clean(self):
        cleaned_data = super(MortgageLoanForm, self).clean()
        return cleaned_data


class RepayForm(forms.ModelForm):
    class Meta:
        model = LoanLog
        fields = ['amount']

    def clean(self):
        cleaned_data = super(RepayForm, self).clean()
        return cleaned_data
