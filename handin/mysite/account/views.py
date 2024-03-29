from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import *
import random
from datetime import *
from log.views import *
from chat.views import chat
from utility.views import *


def account_context(request):
    context = {}
    logs_in = get_log_internal(request)
    logs_ex = get_log_external(request)
    profile = request.user.profile
    account = Account.objects.get(profile=profile)
    checking = account.checking_account.balance
    saving = account.saving_account.balance
    logs = logs_in + logs_ex
    description = []
    for log in logs:
        if log['type'] == 'C':
            log['description'] = "Saving to Checking"
        if log['type'] == 'S':
            log['description'] = "Checking to Saving"
        if log['type'] == 'T':
            log['description'] = log['account_2']

    context['on_line'] = chat(request)
    context['checking_logs'] = logs
    context['saving_logs'] = logs_in
    context['checking'] = checking
    context['saving'] = saving
    context['description'] = description
    context['log_time'] = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
    context['checknumber'] = account.checking_account.account_number
    context['savingnumber'] = account.saving_account.account_number
    context['number'] = account.account_number
    return context


@login_required
def view_accounts(request,context):
    context = account_context(request)

    return render(request, 'account.html', context)

# add external log
def add_log_external(type, amount, account_number_1, account_number_2):
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

# add internal log
def add_log_internal(type, amount, user_name):
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

@login_required
def createAccount(request):
    err_message = []
    message = []
    context = {}
    if request.user.profile.type == 'C':
        err_message.append('you have no permission to do this, plz connect us')
        context = {'message': message, 'err_message': err_message, 'User': request.user}
        return render(request, 'account/err.html', context)
    if request.method == 'POST':
        form = createForm(request.POST)
        context['form'] = form
        context['User'] = request.user
        context['on_line'] = chat(request)
        if not form.is_valid():
            return render(request, 'account/create_account.html', context)
        else:
            new_account = Account(profile = get_object_or_404(User, username = form.cleaned_data['username']).profile,
                                  account_number = request.POST['account_number'],
                                  account_status = 'active')
            new_account.save()

            account_number = random.randint(0, 9999999999)
            while Checking_Account.objects.filter(account_number = account_number):
                account_number = random.randint(0, 9999999999)

            new_checking_account = Checking_Account(account_number= account_number,
                                                    account = new_account,
                                                    balance = 0)
            new_checking_account.save()

            account_number = random.randint(0, 9999999999)
            while Checking_Account.objects.filter(account_number=account_number):
                account_number = random.randint(0, 9999999999)

            new_saving_account = Saving_Account(account_number = account_number,
                                                account = new_account,
                                                balance = 0)
            new_saving_account.save()

            message.append("create " + request.POST['account_number'] + " successfully!" )
            context = {'message': message, 'err_message': err_message, 'User': request.user}
            return view_accounts(request,context)

    else:
        form = createForm()
        context = {'message': message, 'err_message': err_message, 'User': request.user, 'form': form}
        return render(request, 'account/create_account.html', context)

@login_required
@transaction.atomic
def transfer(request):
    err_message = []
    message = []
    context = {}
    context['on_line'] = chat(request)
    if request.method == 'GET':
        context['form'] = TransferForm()

        context['User'] = request.user
        #context['balance'] = request.user.profile.
        return render(request, 'account/transfer.html', context)
    else:
        form = TransferForm(request.POST)
        if is_frozen(request.user.profile):
            err_message.append("your account has already been frozen, plz connect us to deal with this")
            context = {'message': message, 'err_message': err_message, 'User': request.user, 'form': form}
            return render(request, 'account/transfer.html', context)

        context['form'] = form
        context['User'] = request.user
        if not form.is_valid():
            return render(request, 'account/transfer.html', context)

        owner = request.user.profile.account.checking_account
        amount = form.cleaned_data['balance']
        if not is_enough(owner, amount):
            err_message.append("you don't have enough money")
            context = {'message': message, 'err_message': err_message, 'User': request.user, 'form':form}
            return render(request, 'account/transfer.html', context)
        else:
            owner.balance = owner.balance - form.cleaned_data['balance']
            owner.save()
            getter = get_object_or_404(Checking_Account, account_number=form.cleaned_data['target_account'])

            if is_frozen(getter):
                err_message.append("the target account has already been frozen, plz connect us to deal with this")
                context = {'message': message, 'err_message': err_message, 'User': request.user, 'form': form}
                return render(request, 'account/transfer.html', context)
            getter.balance = getter.balance + form.cleaned_data['balance']


            getter.save()
            add_log_external(type='T',
                             amount=form.cleaned_data['balance'],
                             account_number_1=owner.account_number,
                             account_number_2=getter.account_number)
            message.append("you successfully transfer money to " + str(form.cleaned_data['target_account']))
            context = {'message': message, 'err_message': err_message, 'User': request.user}
            #return render(request, 'account/suceed.html', context)
            return view_accounts(request)


@login_required
@transaction.atomic
def transfer_1(request):
    context = {}
    err_message = []
    context['err_message'] = err_message
    context['User'] = request.user
    context['on_line'] = chat(request)
    if request.method == 'GET':
        context['form'] = TransferForm1()
        return render(request, 'account/transfer_1.html', context)
    else:
        form = TransferForm1(request.POST)
        context['form'] = form
        if is_frozen(request.user.profile):
            err_message.append("your account has already been frozen, plz connect us to deal with this")
            return render(request, 'account/transfer_1.html', context)

        if not form.is_valid():
            return render(request, 'account/transfer_1.html', context)

        target_account = form.cleaned_data['target_account']
        getter = Checking_Account.objects.filter(account_number=target_account)
        if len(getter) == 0:
            getter = Saving_Account.objects.filter(account_number=target_account)

        getter = getter[0]

        if is_frozen(getter):
            err_message.append("the target account has already been frozen, plz connect us to deal with this")
            return render(request, 'account/transfer_1.html', context)

        context['target_account'] = form.cleaned_data['target_account']
        context['target_first_name'] = form.cleaned_data['target_first_name']
        context['target_last_name'] = form.cleaned_data['target_last_name']
        return render(request, 'account/transfer_2.html', context)


@login_required
@transaction.atomic
def transfer_2(request):
    context = {}
    err_message = []
    context['err_message'] = err_message
    context['User'] = request.user
    context['on_line'] = chat(request)
    if 'select_account' not in request.GET:
        err_message.append("Please select an account.")
        return render(request, "account/transfer_2.html", context)

    select = request.GET['select_account']
    main_account = request.user.profile.account
    if select == "checking":
        account = main_account.checking_account.account_number
    elif select == "saving":
        account = main_account.saving_account.account_number
    else:
        err_message.append("Account invalid.")
        return render(request, "account/transfer_2.html", context)

    context['target_account'] = request.GET['target_account']
    context['target_first_name'] = request.GET['target_first_name']
    context['target_last_name'] = request.GET['target_last_name']
    context['select'] = select
    context['account'] = account
    context['form'] = TransferForm3()
    return render(request, "account/transfer_3.html", context)


@login_required
@transaction.atomic
def transfer_3(request):
    context = {}
    err_message = []
    context['err_message'] = err_message
    context['User'] = request.user
    form = TransferForm3(request.POST)
    context['form'] = form
    context['on_line'] = chat(request)
    if not form.is_valid():
        return render(request, 'account/transfer_3.html', context)

    owner_account = request.POST['account']
    owner = Saving_Account.objects.filter(account_number=owner_account)
    if len(owner) == 0:
        owner = Checking_Account.objects.filter(account_number=owner_account)

    owner = owner[0]
    amount = form.cleaned_data['balance']

    if not is_enough(owner, amount):
        err_message.append("you don't have enough money")
        return render(request, 'account/transfer_3.html', context)

    owner.balance = owner.balance - amount
    owner.save()

    target_account = request.POST['target_account']
    getter = Checking_Account.objects.filter(account_number=target_account)
    if len(getter) == 0:
        getter = Saving_Account.objects.filter(account_number=target_account)

    getter = getter[0]

    getter.balance = getter.balance + amount

    getter.save()
    add_log_external(type='T',
                     amount=form.cleaned_data['balance'],
                     account_number_1=owner.account_number,
                     account_number_2=getter.account_number)

    context['target_account'] = request.POST['target_account']
    context['target_first_name'] = request.POST['target_first_name']
    context['target_last_name'] = request.POST['target_last_name']
    context['account'] = request.POST['account']
    context['select'] = request.POST['select']
    context['amount'] = amount
    context['description'] = request.POST['description']
    context['profile'] = request.user.profile
    context['time'] = datetime.now()
    return render(request, 'account/transfer_4.html', context)


@login_required
@transaction.atomic
def transfer_4(request):
    context = {}
    context['target_account'] = request.POST['target_account']
    context['target_first_name'] = request.POST['target_first_name']
    context['target_last_name'] = request.POST['target_last_name']
    context['account'] = request.POST['account']
    context['select'] = request.POST['select']
    context['amount'] = request.POST['amount']
    context['description'] = request.POST['description']
    context['time'] = request.POST['time']
    context['on_line'] = chat(request)
    return render(request, "account/transfer_confirm.html", context)


@login_required
@transaction.atomic
def check_to_saving(request):
    err_message = []
    message = []
    context = {}
    context['on_line'] = chat(request)
    if request.method == 'GET':
        context = {'message': message, 'err_message': err_message, 'User': request.user, 'form': csForm()}
        return render(request, 'account/check_to_saving.html', context)
    else:
        form = csForm(request.POST)
        if is_frozen(request.user.profile):
            err_message.append("your account has already been frozen, plz connect us to deal with this")
            context = {'message': message, 'err_message': err_message, 'User': request.user, 'form': form}
            return render(request, 'account/check_to_saving.html', context)
        context['form'] = form
        context['User'] = request.user
        if not form.is_valid():
            return render(request, 'account/check_to_saving.html',context)

        owner_check = request.user.profile.account.checking_account
        owner_saving = request.user.profile.account.saving_account

        amount = form.cleaned_data['balance']
        if not is_enough(owner_check, amount):
            err_message.append("you don't have enough money")
            context = {'message': message, 'err_message': err_message, 'User': request.user, 'form': csForm()}
            return render(request, 'account/check_to_saving.html', context)
        else:
            owner_check.balance = owner_check.balance - amount
            owner_saving.balance = owner_saving.balance + amount
            owner_saving.save()
            owner_check.save()
            add_log_internal(type='S',
                             amount=amount,
                             user_name=request.user.username)
            message.append("you successfully transfer money from check to saving account")
            context = {'message': message, 'err_message': err_message, 'User': request.user}
            #return render(request, 'account/suceed.html', context)
            return view_accounts(request, context)


@login_required
@transaction.atomic
def saving_to_check(request):
    err_message = []
    message = []
    context = {}
    context['on_line'] = chat(request)
    if request.method == 'GET':
        context = {'message': message, 'err_message': err_message, 'User': request.user, 'form': csForm()}
        return render(request, 'account/saving_to_check.html', context)
    else:
        form = csForm(request.POST)
        if is_frozen(request.user.profile):
            err_message.append("your account has already been frozen, plz connect us to deal with this")
            context = {'message': message, 'err_message': err_message, 'User': request.user, 'form': form}
            return render(request, 'account/saving_to_check.html', context)
        context['form'] = form
        context['User'] = request.user
        if not form.is_valid():
            return render(request, 'account/saving_to_check.html', context)

        owner_check = request.user.profile.account.checking_account
        owner_saving = request.user.profile.account.saving_account

        amount = form.cleaned_data['balance']
        if not is_enough(owner_saving, amount):
            err_message.append("you don't have enough money")
            context = {'message': message, 'err_message': err_message, 'User': request.user, 'form': csForm()}
            return render(request, 'account/saving_to_check.html', context)
        else:
            owner_check.balance = owner_check.balance + amount
            owner_saving.balance = owner_saving.balance - amount
            owner_saving.save()
            owner_check.save()
            add_log_internal(type='C',
                                       amount=amount,
                                       user_name=request.user.username)
            message.append("you successfully transfer money from saving to check account")
            context = {'message': message, 'err_message': err_message, 'User': request.user}
            #return render(request, 'account/suceed.html', context)
            return view_accounts(request,context)


@login_required
def freeze_account(request, user_id):
    err_message = []
    message = []
    if request.method == 'POST':
        operator = request.user.profile

        user = get_object_or_404(User, id = user_id)
        if operator.type == 'C' or user.profile.type == 'E':
            err_message.append('you have no permission to do that')
            context = {'message': message, 'err_message': err_message, 'User': request.user}
            return render(request, 'account/err.html', context)

        profile = Profile.objects.get(user = user)
        account = Account.objects.get(profile = profile)
        account.account_status = 'frozen'
        account.save()
        message.append('user ' + user.username + ' has already been frozen')
        context = {'message': message, 'err_message': err_message, 'User': request.user}
        return render (request, 'account/suceed.html', context)
