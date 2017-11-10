# from django import forms
# from django.contrib.auth.models import User
# from models import *
#
# class TransferForm(forms.Form):
#     amount = forms.IntegerField(min_value = 0, label="Transfer Amount")
#     target_user_name = forms.CharField(max_length=100, label="Target Username")
#     target_account = forms.IntegerField(label="Target Account Number")
#
#     def clean(self):
#         cleaned_data = super(TransferForm, self).clean()
#         target_account = cleaned_data.get('targat_account')
#         account = Checking_Account.objects.filter(account_number=target_account)
#         if len(account) == 0:
#             raise forms.ValidationError("No such account!!")
#         else:
#             name = cleaned_data.get('target_user_name')
#             name2 = account[0].account
#             if name.lower() != name2.lower():
#








