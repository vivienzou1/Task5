from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.loan, name="loan"),
    url(r'^auto$', views.auto_loan, name="auto_loan"),
    url(r'^mortgage$', views.mortgage_loan, name="mortgage_loan"),
    url(r'^auto_apply_1$', views.auto_apply_1, name="auto_apply_1"),
    url(r'^auto_apply_2$', views.auto_apply_2, name="auto_apply_2"),
    url(r'^auto_apply_3$', views.auto_apply_3, name="auto_apply_3"),
    url(r'^mortgage_apply$', views.mortgage_apply, name="mortgage_apply"),
    url(r'^repay$', views.repay, name="repay"),
]