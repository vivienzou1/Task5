from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from models import *
from account.models import Account, Checking_Account, Saving_Account
from django.http import HttpResponse
from forms import *
from account import views as account_views
from account.forms import *


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
    account = Account.objects.get(user=user)
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
        amount = request.POST['balance']
        user = request.user
        account = Account.objects.get(user=user)
        account_1 = Checking_Account.objects.get(account=account)
        account_number_1 = account_1.account_number
        account_number_2 = request.POST['target_account']
        context = add_log_external(type, amount, account_number_1, account_number_2)
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
        context = add_log_internal(type, amount, user.username)
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
def get_log_external(request, user_name):
    type = 'all'
    context = {}
    errors = []
    if request.method == "POST":
        try:
            user = get_object_or_404(User, username=user_name)
            account = Account.objects.get(user=user)
            checking_account = Checking_Account.objects.get(account=account)
            logs = LogExternal.objects.filter(account_1=checking_account) | LogExternal.objects.filter(account_2=checking_account)
            if type is "transfer":
                logs = logs.filter(type="T")
            if type is "deposit":
                logs = logs.filter(type="D")
            if type is "withdraw":
                logs = logs.filter(type="W")
            r = construct_json_external(request, logs)
            r = r.replace('\n', ' ').replace('\r', '')
            return render(request, 'log.html', {'context': r})
        except:
            errors.append("error")
            context['errors'] = errors
            pass

    return render(request, 'log.html', {'context': r})


# get internal log (transfer between accounts)
@login_required
def get_log_internal(request, user_name):
    type = 'all'
    context = {}
    errors = []
    if request.method == "POST":
        try:
            user = get_object_or_404(User, username=user_name)
            logs = LogInternal.objects.filter(user=user)
            if type is "toChecking":
                logs = logs.filter(type="C")
            if type is "toSaving":
                logs = logs.filter(type="S")
            r = construct_json_internal(request, logs)
            r = r.replace('\n', ' ').replace('\r', '')
            return render(request, 'log.html', {'context': r})
        except:
            errors.append("error")
            context['errors'] = errors
            pass

    return render(request, 'log.html', {'context': r})





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


# construct external logs to json
def construct_json_external(request, logs):
    r = '['
    for log in logs:
        r = r + '{"pk": ' + str(log.id) + ', '
        r = r + '"type": "' + log.type + '", '
        r = r + '"amount": ' + str(log.amount) + ', '
        r = r + '"account_1": ' + str(log.account_1.account_number) + ', '
        r = r + '"account_2": ' + str(log.account_2.account_number) + ', '
        r = r + '}, '
    if len(logs) != 0:
        r = r[0:len(r) - 2]
    r = r + ']'
    r = r[0: len(r) - 1] + ',{"username":"' + request.user.username + '"}]'
    return r


# construct internal logs to json
def construct_json_internal(request, logs):
    r = '['
    for log in logs:
        r = r + '{"pk": ' + str(log.id) + ', '
        r = r + '"type": "' + log.type + '", '
        r = r + '"amount": ' + str(log.amount) + ', '
        r = r + '}, '
    if len(logs) != 0:
        r = r[0:len(r) - 2]
    r = r + ']'
    r = r[0: len(r) - 1] + ',{"username":"' + request.user.username + '"}]'
    return r
