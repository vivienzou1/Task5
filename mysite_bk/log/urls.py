from django.conf.urls import url
from log import views
from account import views as account_views


urlpatterns = [
    url(r'^create/$', views.test_create, name="create_account"),
    url(r'^transfer/$', views.test_transfer, name="transfer"),
    url(r'^toSaving/$', views.test_check_to_saving, name="show_accounts"),
    url(r'^external/', views.get_log_external, name="get_log_external"),
    url(r'^internal/', views.get_log_internal, name="get_log_internal"),
    url(r'^delete_external/', views.test_delete_external, name="delete_external"),
    url(r'^delete_internal/', views.test_delete_internal, name="delete_internal"),
    url(r'^show/$', views.show_logs, name="show_logs"),
    url(r'^download/$', views.download, name="download"),
]