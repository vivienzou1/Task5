from django.conf.urls import url
from log import views


urlpatterns = [
    url(r'^test/$', views.test, name="test"),
]