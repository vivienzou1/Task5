from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    url(r'^$', views.chat),
    url('^chat/(?P<user_id>\d+)',views.chatwith),
    url(r'^connect/(?P<user_id>\d+)', views.connect),
]