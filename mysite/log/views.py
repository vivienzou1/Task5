from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from forms import *
from account.forms import *
from account.models import *
from django.http import HttpResponse
import unicodecsv


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