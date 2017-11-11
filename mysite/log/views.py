from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from models import *
from account.models import Account, Checking_Account
from django.http import HttpResponse
from forms import *


def test(request):
    form1 = ExternalLogForm()
    form2 = InternalLogForm()
    return render(request, 'test.html', {'form': form1})


@login_required
def get_log_external(request, user_name):
    user = get_object_or_404(User, username=user_name)
    account = Account.objects.get(user=user)
    checking_account = Checking_Account.objects.get(account=account)
    logs = LogExternal.objects.filter(account_1=checking_account) | LogExternal.objects.filter(account_2=checking_account)
    r = construct_json_external(request, logs)
    r = r.replace('\n', ' ').replace('\r', '')
    return HttpResponse(r, content_type='application/json')


@login_required
def get_log_internal(request, user_name):
    user = get_object_or_404(User, username=user_name)
    logs = LogInternal.objects.filter(user=user)
    r = construct_json_internal(request, logs)
    r = r.replace('\n', ' ').replace('\r', '')
    return HttpResponse(r, content_type='application/json')


def add_log_external(request, type, amount, account_1, account_2):
    new_log_external = LogExternal(type=type,
                                   amount=amount,
                                   account_1=account_1,
                                   account_2=account_2,)
    new_log_external.save()


def add_log_internal(request, type, amount, user):
    new_log_internal = LogInternal(type=type,
                                   amount=amount,
                                   user=user)
    new_log_internal.save()


def construct_json_external(request, logs):
    r = '['
    for log in logs:
        r = r + '{"pk": ' + str(log.id) + ', '
        r = r + '"type": "' + log.type + '", '
        r = r + '"amount": "' + log.amount + '", '
        r = r + '"account_1": "' + log.account_1 + '", '
        r = r + '"account_2": "' + log.account_2 + '", '
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
        r = r + '"amount": "' + log.amount + '", '
        r = r + '"user": "' + log.user + '", '
        r = r + '}, '
    if len(logs) != 0:
        r = r[0:len(r) - 2]
    r = r + ']'
    r = r[0: len(r) - 1] + ',{"username":"' + request.user.username + '"}]'
    return r
