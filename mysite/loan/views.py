from django.contrib.auth.decorators import login_required
from .forms import *
from django.shortcuts import render


def loan(request):
    context={}
    errors = []
    context['errors'] = errors
    loans = Loan.objects.filter(profile=request.user.profile)
    context['loans'] = loans
    return render(request, 'loan.html', context)


def auto_loan(request):
    return render(request, 'auto_loan.html', {})


def mortgage_loan(request):
    return render(request, 'mortgage_loan.html', {})


def auto_apply(request):
    context = {}
    errors = []
    context['errors'] = errors
    form = AutoLoanForm(request.POST)
    context['form'] = form
    if request.method == 'GET':
        return render(request, 'auto_apply.html', context)

    if not form.is_valid():
        context['message'] = form.errors
        return render(request, 'auto_apply.html', context)

    profile = request.user.profile
    new_loan = Loan(
        profile=profile,
        type='A',
        amount=form.cleaned_data['amount'],
        cur_amount=form.cleaned_data['amount'],
        period=form.cleaned_data['period'],
        interest=0.001,
    )
    new_loan.save()
    return render(request, 'auto_confirm.html', context)


def mortgage_apply(request):
    context = {}
    errors = []
    context['errors'] = errors
    form = MortgageLoanForm(request.POST)
    context['form'] = form
    if request.method == 'GET':
        return render(request, 'mortgage_apply.html', context)

    if not form.is_valid():
        context['message'] = form.errors
        return render(request, 'mortgage_apply.html', context)

    profile = request.user.profile
    new_loan = Loan(
        profile=profile,
        type='M',
        amount=form.cleaned_data['amount'],
        cur_amount=form.cleaned_data['amount'],
        period=form.cleaned_data['period'],
        interest=0.001,
    )
    new_loan.save()
    return render(request, 'mortgage_confirm.html', context)


def repay(request):
    context = {}
    errors = []
    context['errors'] = errors
    loan = Loan.objects.get(pk=request.GET['loan'])
    context['loan'] = loan
    form = RepayForm(request.POST)
    context['form'] = form
    if request.method == "GET":
        return render(request, 'repay.html', context)
    if not form.is_valid():
        context['message'] = form.errors
        return render(request, 'repay.html', context)

    loan.cur_amount = loan.cur_amount - form.cleaned_data['amount']
    loan.save()

    new_loan_log = LoanLog(
        loan=loan,
        amount=form.cleaned_data['amount'],
        interest='0.001',
    )

    new_loan_log.save()
    return render(request, 'repay_confirm.html', context)
