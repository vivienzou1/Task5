from django import forms
from models import *


class LogForm(forms.ModelForm):
    class Meta:
        model = LogOtherPeople
        fields = ['type',
                  'amount']

    account_number_1 = forms.CharField()
    account_number_2 = forms.CharField()


