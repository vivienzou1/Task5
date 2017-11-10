from django.conf.urls import url, include
from myapp import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^$', views.home),
    url(r'^', include('myapp.urls')),
    url(r'^account/' , include('account.urls'))
]