from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from models import *
from django.contrib.auth.decorators import login_required

@login_required
def createAccount(request):
    err_message = []
    message = []
    context = {}
    if request.method == 'POST':
        if (request.account_number):
            new_account = Account(user = request.user,
                                  account_number = request.account_number,
                                  account_status = 'active')
            new_account.save()

            new_checking_account = Checking_Account(account = new_account,
                                                    balance = 0)
            new_checking_account.save()

            new_saving_account = Saving_Account(account = new_account,
                                                balance = 0)
            new_saving_account.save()

            message.append("create " + request.account_number + " successfully!" )
            context = {'message': message, 'err_message': err_message, 'User': request.user}
            return render(request, 'account/home.html', context)
        else:
            err_message.append("plz enter account number to create an account")
            context = {'message': message, 'err_message': err_message, 'User': request.user }
            return render(request, 'account/create_account.html', context)
    else:
        context = {'message': message, 'err_message': err_message, 'User': request.user}
        return render(request, 'account/create_account.html', context)


@login_required()
def transfer(request):
    err_message = []
    message = []
    context = {}
    if request.method == 'GET':
        return None