# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.models import User
# from models import *
# from django.contrib.auth.decorators import login_required
#
# @login_required
# def createAccount(request):
#     err_message = []
#     message = []
#     context = {}
#     if request.method == 'POST':
#         if (request.account_number):
#             new_account = Account(user = request.user,
#                                   account_number = request.account_number,
#                                   account_status = 'active')
#             new_account.save()
#
#             new_checking_account = Checking_Account(account = new_account,
#                                                     balance = 0)
#             new_checking_account.save()
#
#             new_saving_account = Saving_Account(account = new_account,
#                                                 balance = 0)
#             new_saving_account.save()
#
#             message.append("create " + request.account_number + " successfully!" )
#             context = {'message': message, 'err_message': err_message, 'User': request.user}
#             return render(request, 'account/home.html', context)
#         else:
#             err_message.append("plz enter account number to create an account")
#             context = {'message': message, 'err_message': err_message, 'User': request.user }
#             return render(request, 'account/create_account.html', context)
#     else:
#         context = {'message': message, 'err_message': err_message, 'User': request.user}
#         return render(request, 'account/create_account.html', context)
#
#
# @login_required()
# def transfer(request):
#     err_message = []
#     message = []
#     context = {}
#     if request.method == 'GET':
#         return None

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from models import *
from django.contrib.auth.decorators import login_required
from forms import *
import random
from registration.models import Profile

@login_required
def createAccount(request):
    err_message = []
    message = []
    context = {}
    if request.method == 'POST':
        if (request.account_number):
            if not Account.objects.filter(account_number=request.account_number):
                new_account = Account(user = request.user,
                                      account_number = request.account_number,
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

                message.append("create " + request.account_number + " successfully!" )
                context = {'message': message, 'err_message': err_message, 'User': request.user}
                return render(request, 'account/home.html', context)
            else:
                err_message.append("account has already been used")
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
def transfer(request):
    err_message = []
    message = []
    context = {}
    if request.method == 'GET':
        context['form'] = TransferForm()

        context['User'] = request.user
        return render(request, 'account/transfer.html', context)
    else:
        form = TransferForm(request.POST)
        context['form'] = form
        if not form.is_valid():
            return render(request, 'account/transfer.html', context)

        profile = Profile.objects.get(user=request.user)
        account = Account.objects.get(profile=profile)
        owner = Checking_Account.objects.get(account = account)
        if owner.balance < form.cleaned_data['amount']:
            err_message.append("you don't have enough money")
            context = {'message': message, 'err_message': err_message, 'User': request.user, 'form':form}
            return render(request, 'account/transfer.html', context)
        else:
            owner.balance = owner.balance - form.cleaned_data['amount']

            getter = Checking_Account.objects.get(account_number=form.cleaned_data['target_account'])

            getter.balance = getter.balance + form.cleaned_data['amount']

            owner.save()
            getter.save()
            message.append("you successfully transfer money to " + form.cleaned_data['target_account'])
            context = {'message': message, 'err_message': err_message, 'User': request.user}
            return render(request, 'account/suceed.html', context)

def check_to_saving(request):
    err_message = []
    message = []
    context = {}
    if request.method == 'GET':
        context = {'message': message, 'err_message': err_message, 'User': request.user}
        return render(request, 'account/check_to_saving.html', context)
    else:
        profile = Profile.objects.get(user=request.user)
        account = Account.objects.get(profile=profile)
        owner_check = Checking_Account.objects.get(account=account)
        owner_saving = Saving_Account.objects.get(account=account)
        if owner_check.balance < request.POST['amount']:
            err_message.append("you don't have enough money")
            context = {'message': message, 'err_message': err_message, 'User': request.user}
            return render(request, 'account/check_to_saving.html', context)
        else:
            owner_check.balance = owner_check.balance - request.POST['amount']
            owner_saving.balance = owner_saving.balance + request.POST['amount']
            owner_saving.save()
            owner_check.save()
            message.append("you successfully transfer money from check to saving account")
            context = {'message': message, 'err_message': err_message, 'User': request.user}
            return render(request, 'account/suceed.html', context)