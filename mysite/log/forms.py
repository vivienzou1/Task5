from django import forms
from models import *


# testing LogExternal
class ExternalLogForm(forms.ModelForm):
    class Meta:
        model = LogExternal
        fields = ['type',
                  'amount']

    account_number_1 = forms.CharField()
    account_number_2 = forms.CharField()


# testing LogInternal
class InternalLogForm(forms.ModelForm):
    class Meta:
        model = LogInternal
        fields = ['type',
                  'amount']


