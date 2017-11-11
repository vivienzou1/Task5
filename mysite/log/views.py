from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from models import *
from account.models import Account, Checking_Account, Saving_Account
from django.http import HttpResponse
from forms import *
from account import views as account_views
from account.forms import *


def test_external(request):
    context = {}
    if request.method == 'GET':
        context['form'] = ExternalLogForm()
        return render(request, 'test.html', context)
    else:
        form = ExternalLogForm(request.POST)
        context['form'] = form
        if not form.is_valid():
            return render(request, 'test.html', context)
        result = add_log_external(request,
                                  form.cleaned_data['type'],
                                  form.cleaned_data['amount'],
                                  form.cleaned_data['account_number_1'],
                                  form.cleaned_data['account_number_2'])
        message = "log added"
        context['message'] = message
        context['result'] = result
    return render(request, 'test.html', {'result': result})


# show the user's account numbers (account, checking, saving)
def show_accounts(request):
    context = {}
    user = request.user
    account = Account.objects.get(user=user)
    checking_account = Checking_Account.objects.get(account=account)
    saving_account = Saving_Account.objects.get(account=account)
    context['account'] = account.account_number
    context['checking_account'] = checking_account.account_number
    context['saving_account'] = saving_account.account_number
    return render(request, 'show_accounts.html', context)


def show_logs(request):
    return render(request, 'log.html', {})


def test_internal(request):
    context = {}
    if request.method == 'GET':
        context['form'] = InternalLogForm()
        return render(request, 'test.html', context)
    else:
        form = InternalLogForm(request.POST)
        context['form'] = form
        if not form.is_valid():
            return render(request, 'test.html', context)
        result = add_log_internal(request,
                                  form.cleaned_data['type'],
                                  form.cleaned_data['amount'],
                                  request.user.username)
        message = "log added"
        context['message'] = message
        context['result'] = result
    return render(request, 'test.html', {'result': result})


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_number']


def test_create(request):
    form = AccountForm
    if request.method == 'GET':
        return render(request, 'create.html', {'form': form})
    else:
        request.account_number = request.POST['account_number']
        return account_views.createAccount(request)


def test_transfer(request):
    form = TransferForm
    if request.method == 'GET':
        return render(request, 'test_transfer.html', {'form': form})
    else:
        type = 'transfer'
        amount = request.POST['balance']
        user = request.user
        print user.username
        account = Account.objects.get(user=user)
        print account.account_number
        account_1 = Checking_Account.objects.get(account=account)
        account_number_1 = account_1.account_number
        print account_number_1
        account_number_2 = request.POST['target_account']
        print account_number_2
        context = add_log_external(request, type, amount, account_number_1, account_number_2)
        print context
        return render(request, 'test_transfer.html', context)


class CheckToSavingForm(forms.Form):
    amount = forms.IntegerField()


def test_check_to_saving(request):
    form = CheckToSavingForm
    if request.method == 'GET':
        return render(request, 'test_transfer.html', {'form': form})
    else:
        type = 'toSaving'
        amount = request.POST['amount']
        user = request.user
        context = add_log_internal(request, type, amount, user.username)
        return render(request, 'test_transfer.html', {'context': context})


@login_required
def get_log_external(request, user_name):
    type = 'all'
    context = {}
    errors = []
    if request.method == "POST":
        try:
            user = get_object_or_404(User, username=user_name)
            print user.username
            account = Account.objects.get(user=user)
            print account.account_number
            checking_account = Checking_Account.objects.get(account=account)
            print checking_account.account_number
            print LogExternal.objects.filter(account_1=checking_account) | LogExternal.objects.filter(account_2=checking_account)
            logs = LogExternal.objects.filter(account_1=checking_account) | LogExternal.objects.filter(
                account_2=checking_account)
            print logs[0]
            print logs[0].account_1.account_number
            if type is "transfer":
                logs = logs.filter(type="T")
                print "t"
            if type is "deposit":
                logs = logs.filter(type="D")
            if type is "withdraw":
                logs = logs.filter(type="W")
            r = construct_json_external(request, logs)
            r = r.replace('\n', ' ').replace('\r', '')
            return HttpResponse(r, content_type='application/json')
        except:
            errors.append("error")
            context['errors'] = errors
            pass

    return HttpResponse(context, content_type='application/json')


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
            print r
            r = r.replace('\n', ' ').replace('\r', '')
            return HttpResponse(r, content_type='application/json')
        except:
            errors.append("error")
            context['errors'] = errors
            pass

    return HttpResponse(context, content_type='application/json')


def add_log_external(request, type, amount, account_number_1, account_number_2):
    context = {}
    errors = []
    try:
        account_1 = Checking_Account.objects.get(account_number=account_number_1)
        print "account1"
        account_2 = Checking_Account.objects.get(account_number=account_number_2)
        print "account2"
        new_log_external = LogExternal(type=type,
                                       amount=amount,
                                       account_1=account_1,
                                       account_2=account_2,
                                       )
        print "new"
        new_log_external.save()
        print "save"
        success = True
    except ObjectDoesNotExist:
        errors.append("Object does not exist.")
        success = False
        pass
    context['success'] = success
    context['errors'] = errors
    return context


def add_log_internal(request, type, amount, user_name):
    context = {}
    errors = []
    try:
        user = User.objects.get(username=user_name)
        new_log_internal = LogInternal(type=type,
                                       amount=amount,
                                       user=user)
        new_log_internal.save()
        success = True
    except ObjectDoesNotExist:
        errors.append("Object does not exist.")
        success = False
        pass
    context['success'] = success
    context['errors'] = errors
    return context


def delete_log_external(request, log_id):
    context = {}
    errors = []
    if request.method == 'POST':
        try:
            log_to_delete = LogExternal.objects.get(id=log_id)
            log_to_delete.delete()
            success = True
        except ObjectDoesNotExist:
            errors.append("Object does not exist.")
            success = False
            pass
    context['success'] = success
    context['errors'] = errors
    return context


def delete_log_internal(request, log_id):
    context = {}
    errors = []
    if request.method == 'POST':
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


def construct_json_external(request, logs):
    print "construct"
    r = '['
    for log in logs:
        print log.account_1.account_number
        r = r + '{"pk": ' + str(log.id) + ', '
        r = r + '"type": "' + log.type + '", '
        r = r + '"amount": ' + str(log.amount) + ', '
        r = r + '"account_1": ' + str(log.account_1.account_number) + ', '
        print log.account_2.account_number
        r = r + '"account_2": ' + str(log.account_2.account_number) + ', '
        r = r + '}, '
    if len(logs) != 0:
        r = r[0:len(r) - 2]
    r = r + ']'
    r = r[0: len(r) - 1] + ',{"username":"' + request.user.username + '"}]'
    return r


def construct_json_internal(request, logs):
    r = '['
    for log in logs:
        r = r + '{"pk": ' + str(log.id) + ', '
        r = r + '"type": "' + log.type + '", '
        r = r + '"amount": ' + str(log.amount) + ', '
        r = r + '"user": "' + log.user.username + '", '
        r = r + '}, '
    if len(logs) != 0:
        r = r[0:len(r) - 2]
    r = r + ']'
    r = r[0: len(r) - 1] + ',{"username":"' + request.user.username + '"}]'
    return r
