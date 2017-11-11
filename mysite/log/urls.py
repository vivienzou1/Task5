from django.conf.urls import url
from log import views


urlpatterns = [
    url(r'^test_external/$', views.test_external, name="test_external"),
    url(r'^test_internal/$', views.test_internal, name="test_internal"),
]