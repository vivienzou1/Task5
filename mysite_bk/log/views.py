from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from registration.models import Profile

from models import *
from account.models import Account, Checking_Account, Saving_Account
from django.http import HttpResponse
from forms import *
from account import views as account_views
from account.forms import *
from account.models import *
import os
from django.conf import settings
from django.http import HttpResponse
import unicodecsv
import json

def show_logs(request):
    return render(request, 'log.html', {})


# simulate opening account
class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_number']


# simulate opening account
def test_create(request):
    form = AccountForm
    if request.method == 'GET':
        return render(request, 'create.html', {'form': form})
    else:
        request.account_number = request.POST['account_number']
        return account_views.createAccount(request)


# get the user's account numbers (account, checking, saving)
def get_accounts(user):
    context = {}
    profile = user.profile
    account = Account.objects.get(profile=profile)
    checking_account = Checking_Account.objects.get(account=account)
    saving_account = Saving_Account.objects.get(account=account)
    context['account'] = account.account_number
    context['checking_account'] = checking_account.account_number
    context['saving_account'] = saving_account.account_number
    return context


# simulate transferring to others
def test_transfer(request):
    form = TransferForm
    if request.method == 'GET':
        return render(request, 'test_transfer.html', {'form': form})
    else:
        type = 'transfer'
        amount = request.POST['balance_0']
        user = request.user
        account = Account.objects.get(profile=user.profile)
        account_1 = Checking_Account.objects.get(account=account)
        account_number_1 = account_1.account_number
        account_number_2 = request.POST['target_account']
        context = account_views.add_log_external(type, amount, account_number_1, account_number_2)
        return render(request, 'test_transfer.html', context)


# simulate transfer from checking to saving
class CheckToSavingForm(forms.Form):
    amount = forms.IntegerField()


# simulate transfer from checking to saving
def test_check_to_saving(request):
    form = CheckToSavingForm
    if request.method == 'GET':
        return render(request, 'test_transfer.html', {'form': form})
    else:
        type = 'toSaving'
        amount = request.POST['amount']
        user = request.user
        context = account_views.add_log_internal(type, amount, user.username)
        return render(request, 'test_transfer.html', {'context': context})


# simulate deleting log
class DeleteForm(forms.Form):
    id = forms.IntegerField()


def test_delete_external(request):
    form = DeleteForm
    if request.method == 'GET':
        return render(request, 'delete_external.html', {'form': form})
    else:
        context = delete_log_external(request.POST['id'])
        return render(request, 'delete_external.html', context)


def test_delete_internal(request):
    form = DeleteForm
    if request.method == 'GET':
        return render(request, 'delete_internal.html', {'form': form})
    else:
        context = delete_log_internal(request.POST['id'])
        return render(request, 'delete_internal.html', context)


# get external log (transfer to others)
@login_required
def get_log_external(request):
    type = 'all'
    context = {}
    errors = []
    r = []
    try:
        user = request.user
        profile = Profile.objects.get(user=user)
        account = Account.objects.get(profile=profile)
        checking_account = Checking_Account.objects.get(account=account)
        logs_1 = LogExternal.objects.filter(account_1=checking_account)
        logs_2 = LogExternal.objects.filter(account_2=checking_account)
        # if type is "transfer":
        #     logs = logs.filter(type="T")
        # if type is "deposit":
        #     logs = logs.filter(type="D")
        # if type is "withdraw":
        #     logs = logs.filter(type="W")
        for log in logs_1:
            print log
            l = {}
            l['pk'] = log.id
            l['type'] = log.type
            l['amount'] = log.amount
            l['account_1'] = log.account_1
            l['account_2'] = log.account_2
            l['time'] = log.created.strftime("%Y-%m-%d")
            l['withdraw'] = log.amount
            l['deposit'] = ""
            l['category'] = "pay"
            r.append(l)
        for log in logs_2:
            l = {}
            l['pk'] = log.id
            l['type'] = log.type
            l['amount'] = log.amount
            l['account_1'] = log.account_1
            l['account_2'] = log.account_2
            l['time'] = log.created.strftime("%Y-%m-%d")
            l['withdraw'] = ""
            l['deposit'] = log.amount
            l['category'] = "receive"
            r.append(l)
        print len(r)
        return r
    except:
        errors.append("error")
        context['errors'] = errors
        pass
    return ""


# get internal log (transfer between accounts)
@login_required
def get_log_internal(request):
    type = 'all'
    context = {}
    errors = []
    r = []
    try:
        user = request.user
        logs = LogInternal.objects.filter(user=user)
        if type is "toChecking":
            logs = logs.filter(type="C")
        if type is "toSaving":
            logs = logs.filter(type="S")
        for log in logs:
            l = {}
            l['pk'] = log.id
            l['type'] = log.type
            l['amount'] = log.amount
            l['time'] = log.created.strftime("%Y-%m-%d")
            l['category'] = "transfer"
            if log.type == "C":
                l['withdraw'] = ""
                l['deposit'] = log.amount
            if log.type == "S":
                l['withdraw'] = log.amount
                l['deposit'] = ""
            r.append(l)
        print r
        return r
    except:
        errors.append("error")
        context['errors'] = errors
        pass
    return ""





# delete external log
def delete_log_external(log_id):
    context = {}
    errors = []
    try:
        log_to_delete = LogExternal.objects.get(pk=log_id)
        log_to_delete.delete()
        success = True
    except ObjectDoesNotExist:
        errors.append("Object does not exist.")
        success = False
        pass
    context['success'] = success
    context['errors'] = errors
    return context


# delete internal log
def delete_log_internal(log_id):
    context = {}
    errors = []
    try:
        log_to_delete = LogInternal.objects.get(id=log_id)
        log_to_delete.delete()
        success = True
    except ObjectDoesNotExist:
        errors.append("Object does not exist.")
        success = False
        pass
    context['success'] = success
    context['errors'] = errors
    return context


# # construct external logs to json
# def construct_json_external(request, logs):
#     r = '['
#     for log in logs:
#         r = r + '{"pk": ' + str(log.id) + ', '
#         r = r + '"type": "' + log.type + '", '
#         r = r + '"amount": ' + str(log.amount) + ', '
#         r = r + '"account_1": ' + str(log.account_1.account_number) + ', '
#         r = r + '"account_2": ' + str(log.account_2.account_number) + ', '
#         r = r + '}, '
#     if len(logs) != 0:
#         r = r[0:len(r) - 2]
#     r = r + ']'
#     r = r[0: len(r) - 1] + ',{"username":"' + request.user.username + '"}]'
#     return r
#
#
# # construct internal logs to json
# def construct_json_internal(request, logs):
#     r = '['
#     for log in logs:
#         # r = r + '{"pk": ' + str(log.id) + ', '
#         # r = r + '"type": "' + log.type + '", '
#         # r = r + '"amount": ' + str(log.amount) + ', '
#         # r = r + '}, '
#         r= r+str("sdfg")+', '
#     if len(logs) != 0:
#         r = r[0:len(r) - 2]
#     r = r + ']'
#     #r = r[0: len(r) - 1] + ',{"username":"' + request.user.username + '"}]'
#     return r


def download(request):
    logs = get_log_internal(request)+get_log_external(request)
    csv = HttpResponse(content_type='text/csv')
    csv['Content-Disposition'] = 'attachment; filename="online_statements.csv"'
    writer = unicodecsv.writer(csv)
    writer.writerow(['Type', 'deposit', 'withdraw', 'time'])

    for log in logs:
        data = []
        data.append(str(log['category']))
        data.append(str(log['deposit']))
        data.append(str(log['withdraw']))
        data.append(str(log['time']))
        writer.writerow(data)
    return csv