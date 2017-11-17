from django.http import Http404
from django.db import transaction
from django.contrib.auth.tokens import default_token_generator
from forms import *
from django.contrib.auth import authenticate, login
from log.views import *
from datetime import datetime
from datetime import timedelta


def home(request):
    return render(request, 'index.html', {})


def user_login(request):
    context = {}
    errors = ""
    context['errors'] = errors

    if request.method == 'GET':
        return render(request, 'login.html', context)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                context = account_context()
                return render(request, 'account.html', context)
            else:
                errors = "You're account is disabled."
        else:
            errors = "Invalid user ID or passcode."

    context['errors'] = errors

    return render(request, 'login.html', context)


@transaction.atomic
def register(request):
    context = {}
    errors = []
    context['errors'] = errors

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'register.html', context)

    form = RegistrationForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        context['message'] = ["ERR: username exist or password don't match"]
        return render(request, 'register.html', context)

    new_user = User.objects.create_user(username=form.cleaned_data['Username'],
                                        password=form.cleaned_data['Password'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'],
                                        email=form.cleaned_data['email'],)

    new_user.is_active = False
    new_user.save()

    token = default_token_generator.make_token(new_user)

    return confirm_registration(request, form, token)


@transaction.atomic
def confirm_registration(request, form, token):
    user = get_object_or_404(User, username=form.cleaned_data['Username'])

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

        # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()

    login(request, user)

    new_profile = Profile(last_name=user.first_name,
                          first_name=user.last_name,
                          user=user,
                          email=user.email,
                          phone=form.cleaned_data['phone'],
                          middle_name=form.cleaned_data['middle_name'],
                          address=form.cleaned_data['address'],
                          date_of_birth=form.cleaned_data['date_of_birth'],
                          gender=form.cleaned_data['gender'],
                          ssn=form.cleaned_data['ssn'],
                          type="client",
                          )
    new_profile.save()

    return render(request, 'account.html', {})


def account_context(request):
    context = {}
    logs_in = get_log_internal(request)
    print logs_in
    logs_ex = get_log_external(request)
    print logs_ex
    profile = request.user.profile
    account = Account.objects.get(profile=profile)
    checking = account.checking_account.balance
    saving = account.saving_account.balance
    logs = logs_in + logs_ex
    description = []
    print logs
    for log in logs:
        print log
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

# @login_required
# def get_profile(request, user_name):
#     user = get_object_or_404(User, username=user_name)
#     user_profile = Profile.objects.filter(user=user)
#     r = construct_json(request, user_profile)
#     r = r.replace('\n', ' ').replace('\r', '')
#     return HttpResponse(r, content_type='application/json')


@login_required
def profile(request):
    errors = []
    context = {}

    user = request.user

    try:
        user_profile = Profile.objects.get(user=user)
        context['profile'] = user_profile
    except:
        errors.append('No such profile')

    context['message'] = errors
    profile = user.profile
    context['first_name'] = profile.first_name
    context['last_name'] = profile.last_name
    context['middle_name'] = profile.middle_name
    context['email'] = profile.email
    context['phone'] = profile.phone
    context['address'] = profile.address
    context['dob'] = profile.date_of_birth
    context['gender'] = profile.gender
    context['ssn'] = profile.ssn

    return render(request, 'profile.html', context)

