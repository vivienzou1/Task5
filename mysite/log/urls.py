from django.conf.urls import url
from log import views
from account import views as account_views


urlpatterns = [
    url(r'^test_external/$', views.test_external, name="test_external"),
    url(r'^test_internal/$', views.test_internal, name="test_internal"),
    url(r'^external/(?P<user_name>.*)', views.get_log_external, name="get_log_external"),
    url(r'^internal/(?P<user_name>.*)', views.get_log_internal, name="get_log_internal"),
    url(r'^show/$', views.show_logs, name="show_logs"),
    url(r'^create/$', views.test_create, name="create_account"),
    url(r'^transfer/$', views.test_transfer, name="transfer"),
    url(r'^toSaving/$', views.test_check_to_saving, name="show_accounts"),
    url(r'^show_accounts/$', views.show_accounts, name="show_accounts"),
]