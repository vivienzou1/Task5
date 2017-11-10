from django.conf.urls import url, include
import views

urlpatterns = [
    url(r'^transfer$', views.transfer, name="transfer"),
]