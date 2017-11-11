from django.conf.urls import url
from log import views


urlpatterns = [
    url(r'^test_external/$', views.test_external, name="test_external"),
    url(r'^test_internal/$', views.test_internal, name="test_internal"),
    url(r'^external/(?P<user_name>.*)', views.get_log_external, name="get_log_external"),
    url(r'^internal/(?P<user_name>.*)', views.get_log_internal, name="get_log_internal"),
    url(r'^show/$', views.show_logs, name="show_logs"),
]