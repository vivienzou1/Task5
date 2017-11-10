from django.conf.urls import url, include
from registration import views
urlpatterns = [
    url(r'^$', views.home),
    url(r'^', include('registration.urls')),
    url(r'^account/', include('account.urls'))
]