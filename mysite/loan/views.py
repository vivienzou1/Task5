from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def loan(request):
    return render(request, 'loan.html', {})


def auto_loan(request):
    return render(request, 'auto_loan.html', {})


def mortgage_loan(request):
    return render(request, 'mortgage_loan.html', {})


def auto_apply(request):
    return render(request, 'auto_apply.html', {})


def mortgage_apply(request):
    return render(request, 'mortgage_apply.html', {})
