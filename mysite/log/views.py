from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from models import *
from account.models import Account, Checking_Account
from django.http import HttpResponse
from forms import *


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


@login_required
def get_log_external(request, user_name, type):
    user = get_object_or_404(User, username=user_name)
    account = Account.objects.get(user=user)
    checking_account = Checking_Account.objects.get(user=user)
    logs = LogExternal.objects.filter(account_1=checking_account) | LogExternal.objects.filter(account_2=checking_account)
    if type is "transfer":
        logs = logs.filter(type="T")
    if type is "deposit":
        logs = logs.filter(type="D")
    if type is "withdraw":
        logs = logs.filter(type="W")
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


def add_log_external(request, type, amount, account_number_1, account_number_2):
    context = {}
    errors = []
    try:
        account_1 = Checking_Account.objects.get(account_number=account_number_1)
        account_2 = Checking_Account.objects.get(account_number=account_number_2)
        new_log_external = LogExternal(type=type,
                                       amount=amount,
                                       account_1=account_1,
                                       account_2=account_2,
                                       )
        new_log_external.save()
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
