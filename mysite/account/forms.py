from django import forms
from django.contrib.auth.models import User


class TransferForm(forms.Form):
    acount_Choice = (
        ('Checking Account', 'checking_account'),
        ('Saving Account', 'saving_account')
    )

    amount = forms.IntegerField(min_value = 0, label="Transfer Amount")
    use_account_type = forms.ChoiceField(choices=acount_Choice, label="Choose what account to use")

    target_user_name = forms.CharField(max_length=100, label="Target Username")
    target_account = forms.IntegerField(label="Target Account Number")
    target_account_type = forms.ChoiceField(choices=acount_Choice, label="Choose what account to transfer")

    def



