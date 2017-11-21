from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^transfer$', views.transfer, name="transfer"),
    url(r'^create_account$', views.createAccount, name='create_account'),
    url(r'^check_to_saving$', views.check_to_saving, name='check_to_saving'),
    url(r'^saving_to_check$', views.saving_to_check, name='saving_to_check'),
    url(r'^freeze_account/(?P<user_id>\d+)', views.freeze_account, name='account_freeze')
]