from django.conf.urls import url
from log import views


urlpatterns = [
    url(r'^all/$', views.all_log, name="all_log"),
]