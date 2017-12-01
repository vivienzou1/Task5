from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    url(r'^$', views.chat, name="chat"),
    url(r'^connect/(?P<user_id>\d+)', views.connect),
]