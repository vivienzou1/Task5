from django import forms
from django.contrib.auth.models import User
from models import *
from django.forms import widgets as Fwidgets
from djmoney.models.fields import MoneyField

class TransferForm(forms.ModelForm):
    class Meta:
        model = Checking_Account
        fields = ('balance',)
        labels = {
            'balance': 'Amount'
        }
        css = {

        }
       #
    target_user_name = forms.CharField(max_length=100, label="Target Username")
    target_account = forms.IntegerField(label="Target Account Number",
                                        widget=forms.TextInput())

    def clean(self):
        cleaned_data = super(TransferForm, self).clean()
        target_account = cleaned_data.get('target_account')
        account = Checking_Account.objects.filter(account_number=target_account)
        if len(account) == 0:
            raise forms.ValidationError("No such account!!")
        else:
            name = cleaned_data.get('target_user_name')

            name2 = account[0].account.profile.last_name + ' '
            if account[0].account.profile.middle_name:
                name2 += account[0].account.profile.middle_name + ' '
            name2 += account[0].account.profile.first_name
            if name.lower() != name2.lower():
                raise  forms.ValidationError("name and account can not match!!")

        return cleaned_data

class csForm(forms.ModelForm):
    class Meta:
        model = Checking_Account
        fields = {'balance',}
        labels = {
            'balance': 'Amount'
        }







