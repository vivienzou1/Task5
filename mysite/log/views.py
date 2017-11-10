from django.shortcuts import render


def all_log(request):
    return render(request, 'all_log.html', {})
