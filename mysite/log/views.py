from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from models import *
from account.models import Account, Checking_Account
from django.http import HttpResponse
from forms import LogForm


def test(request):
    form = LogForm()
    return render(request, 'test.html', {'form': form})


@login_required
def get_log_other_people(request, user_name):
    user = get_object_or_404(User, username=user_name)
    account = Account.objects.get(user=user)
    checking_account = Checking_Account.objects.get(account=account)
    logs = LogOtherPeople.objects.filter(account_1=checking_account) | LogOtherPeople.objects.filter(account_2=checking_account)
    r = construct_json(request, logs)
    r = r.replace('\n', ' ').replace('\r', '')
    return HttpResponse(r, content_type='application/json')


def add_log_other_people(request, type, amount, account_1, account_2):
    new_log_other_people = LogOtherPeople(type=type,
                                          amount=amount,
                                          account_1=account_1,
                                          account_2=account_2,)
    new_log_other_people.save()


def construct_json(request, logs):
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
