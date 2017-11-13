from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from forms import *
import random


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
        if request.POST['account_number']:
            if Account.objects.filter(account_number=request.POST['account_number']):
                err_message.append("account has already been used")
                context = {'message': message, 'err_message': err_message, 'User': request.user}
                return render(request, 'account/create_account.html', context)
            if Account.objects.filter(profile = get_object_or_404(Profile, user = request.user)):
                err_message.append("user has already get an account")
                context = {'message': message, 'err_message': err_message, 'User': request.user}
                return render(request, 'account/create_account.html', context)

            new_account = Account(profile = get_object_or_404(Profile, user = request.user),
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
            err_message.append("plz enter account number to create an account")
            context = {'message': message, 'err_message': err_message, 'User': request.user }
            return render(request, 'account/create_account.html', context)
    else:
        context = {'message': message, 'err_message': err_message, 'User': request.user}
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
            message.append("you successfully transfer money to " + str(form.cleaned_data['target_account']))
            context = {'message': message, 'err_message': err_message, 'User': request.user}
            return render(request, 'account/suceed.html', context)

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
            return render(request, 'account/transfer.html', context)
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
            message.append("you successfully transfer money from check to saving account")
            context = {'message': message, 'err_message': err_message, 'User': request.user}
            return render(request, 'account/suceed.html', context)

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
            return render(request, 'account/transfer.html', context)
        context['form'] = form
        context['User'] = request.user
        if not form.is_valid():
            return render(request, 'account/saving_to_check.html', context)

        owner_check = request.user.profile.account.checking_account
        owner_saving = request.user.profile.account.saving_account

        amount = form.cleaned_data['balance']
        if owner_check.balance < amount:
            err_message.append("you don't have enough money")
            context = {'message': message, 'err_message': err_message, 'User': request.user, 'form': csForm()}
            return render(request, 'account/saving_to_check.html', context)
        else:
            owner_check.balance = owner_check.balance + amount
            owner_saving.balance = owner_saving.balance - amount
            owner_saving.save()
            owner_check.save()
            message.append("you successfully transfer money from saving to check account")
            context = {'message': message, 'err_message': err_message, 'User': request.user}
            return render(request, 'account/suceed.html', context)

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