from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^test$', views.test, name="test"),
    url(r'^transfer$', views.transfer_1, name="transfer_1"),
    url(r'^transfer_2$', views.transfer_2, name="transfer_2"),
    url(r'^transfer_3$', views.transfer_3, name="transfer_3"),
    url(r'^transfer_4$', views.transfer_4, name="transfer_4"),
    url(r'^create_account$', views.createAccount, name='create_account'),
    url(r'^check_to_saving$', views.check_to_saving, name='check_to_saving'),
    url(r'^saving_to_check$', views.saving_to_check, name='saving_to_check'),
    url(r'^freeze_account/(?P<user_id>\d+)', views.freeze_account, name='account_freeze')
]