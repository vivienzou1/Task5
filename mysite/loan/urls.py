from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.loan, name="loan"),
    url(r'^auto$', views.auto_loan, name="auto_loan"),
    url(r'^mortgage$', views.mortgage_loan, name="mortgage_loan"),
    url(r'^auto_apply$', views.auto_apply, name="auto_apply"),
    url(r'^mortgage_apply$', views.mortgage_apply, name="mortgage_apply"),
]