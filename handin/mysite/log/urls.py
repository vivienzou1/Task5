from django.conf.urls import url
from log import views
from account import views as account_views


urlpatterns = [
    url(r'^download/$', views.download, name="download"),
]