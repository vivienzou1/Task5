from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import *
import random
from datetime import *
from log.views import *


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

    context['checking_logs'] = logs
    context['saving_logs'] = logs_in
    context['checking'] = checking
    context['saving'] = saving
    context['description'] = description
    context['log_time'] = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
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
            return render(request, 'account/home.html', context)

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
    if request.method == 'GET':
        context['form'] = TransferForm()

        context['User'] = request.user
        #context['balance'] = request.user.profile.
        return render(request, 'account/transfer.html', context)
    else:
        form = TransferForm(request.POST)
        if request.user.profile.account.account_status == 'frozen':
            err_message.append("your account has already been frozen, plz connect us to deal with this")
            context = {'message': message, 'err_message': err_message, 'User': request.user, 'form': form}
            return render(request, 'account/transfer.html', context)

        context['form'] = form
        context['User'] = request.user
        if not form.is_valid():
            return render(request, 'account/transfer.html', context)

        owner = request.user.profile.account.checking_account
        if owner.balance < form.cleaned_data['balance']:
            err_message.append("you don't have enough money")
            context = {'message': message, 'err_message': err_message, 'User': request.user, 'form':form}
            return render(request, 'account/transfer.html', context)
        else:
            owner.balance = owner.balance - form.cleaned_data['balance']
            owner.save()
            getter = get_object_or_404(Checking_Account, account_number=form.cleaned_data['target_account'])

            if getter.account.account_status == 'frozen':
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


def transfer_1(request):
    err_message = []
    message = []
    context = {}
    if request.method == 'GET':
        context['form'] = TransferForm1()
        context['User'] = request.user
        return render(request, 'account/transfer_1.html', context)
    else:
        form = TransferForm1(request.POST)
        if request.user.profile.account.account_status == 'frozen':
            err_message.append("your account has already been frozen, plz connect us to deal with this")
            context = {'message': message, 'err_message': err_message, 'User': request.user, 'form': form}
            return render(request, 'account/transfer_1.html', context)

        context['form'] = form
        context['User'] = request.user
        if not form.is_valid():
            return render(request, 'account/transfer_1.html', context)
        return render(request, 'account/transfer_2.html', context)

def transfer_2(request):
    err_message = []
    message = []
    context = {}
    value = request.GET['select_account']
    main_account = request.user.profile.account
    if value == 1:
        account = main_account.checking_account
    else:
        account = main_account.saving_account
    return render(request, "account/transfer_3.html", {})


def transfer_3(request):
    err_message = []
    message = []
    context = {}
    form = TransferForm3(request.POST)
    context['form'] = form
    context['User'] = request.user
    if not form.is_valid():
        return render(request, 'account/transfer_3.html', context)
    return render(request, 'account/transfer_4.html', context)

def transfer_4(request):
    return render(request, "account/transfer_4.html", {})


def test(request):
    context = {}
    form = TransferForm3()
    context['form'] = form
    return render(request, "account/test.html", context)

@login_required
@transaction.atomic
def check_to_saving(request):
    err_message = []
    message = []
    context = {}
    if request.method == 'GET':
        context = {'message': message, 'err_message': err_message, 'User': request.user, 'form': csForm()}
        return render(request, 'account/check_to_saving.html', context)
    else:
        form = csForm(request.POST)
        if request.user.profile.account.account_status == 'frozen':
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
        if owner_check.balance < amount:
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
    if request.method == 'GET':
        context = {'message': message, 'err_message': err_message, 'User': request.user, 'form': csForm()}
        return render(request, 'account/saving_to_check.html', context)
    else:
        form = csForm(request.POST)
        if request.user.profile.account.account_status == 'frozen':
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
        if owner_saving.balance < amount:
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
