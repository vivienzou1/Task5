from django import forms
from django.contrib.auth.models import User
from .models import *
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


class TransferForm1(forms.Form):

    target_first_name = forms.CharField(max_length=100, label="Target Firstname", required="True")
    target_last_name = forms.CharField(max_length=100, label="Target Lastname", required="True")
    target_account = forms.IntegerField(label="Target Account Number",
                                        widget=forms.TextInput(), required="True")

    def clean(self):
        cleaned_data = super(TransferForm1, self).clean()
        target_account = cleaned_data.get('target_account')
        account = Checking_Account.objects.filter(account_number=target_account)
        if len(account) == 0:
            account = Saving_Account.objects.filter(account_number=target_account)
        if len(account) == 0:
            raise forms.ValidationError("No such account!!")
        else:
            first_name = cleaned_data.get('target_first_name')
            last_name = cleaned_data.get('target_last_name')

            first_name_0 = account[0].account.profile.first_name
            last_name_0 = account[0].account.profile.last_name

            if (first_name.lower() != first_name_0.lower()) or (last_name.lower() != last_name_0.lower()):
                raise forms.ValidationError("name and account can not match!!")

        return cleaned_data


class TransferForm3(forms.ModelForm):
    class Meta:
        model = Checking_Account
        fields = ('balance',)
        labels = {
            'balance': 'Amount'
        }

    def clean(self):
        cleaned_data = super(TransferForm3, self).clean()
        return cleaned_data


class csForm(forms.ModelForm):
    class Meta:
        model = Checking_Account
        fields = ('balance',)
        labels = {
            'balance': 'Amount'
        }

class createForm(forms.Form):
    username = forms.CharField(max_length=100, label='Username')
    first_name = forms.CharField(max_length=100, label="First Name")
    middle_name = forms.CharField(max_length=100, label="Middle Name", required=False)
    last_name = forms.CharField(max_length=100, label="Last Name")
    account_number = forms.IntegerField(label='Account number',
                                        widget=forms.TextInput())
    def clean(self):
        cleaned_data = super(createForm,self).clean()
        users = User.objects.filter(username = cleaned_data.get('username'))
        if len(users) == 0:
            raise forms.ValidationError("Username is wrong")
        else:
            user = users[0]
            print(user.first_name != cleaned_data.get('first_name'))
            print(user.last_name != cleaned_data.get('last_name'))
            print(user.profile.middle_name == None)
            print(cleaned_data.get('middle_name') == "")
            if user.first_name.lower() != cleaned_data.get('first_name') or user.last_name != cleaned_data.get('last_name'):
                raise forms.ValidationError('name is wrong')
            if cleaned_data.get('middle_name') == "" and user.profile.middle_name != None:
                raise forms.ValidationError('name is wrong')
            if cleaned_data.get('middle_name') != "" and cleaned_data.get('middle_name') ==  user.profile.middle_name:
                raise forms.ValidationError('name is wrong')
            if Account.objects.filter(account_number=cleaned_data.get('account_number')):
                raise forms.ValidationError('account number has already been occupied')
            if Account.objects.filter(profile=user.profile):
                raise forms.ValidationError('user has already get an account')

        return cleaned_data





