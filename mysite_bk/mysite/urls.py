from django.conf.urls import url, include
from registration import views
from django.contrib import admin
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home),
    url(r'^', include('registration.urls')),
    url(r'^log/', include('log.urls')),
    url(r'^account/', include('account.urls'))
]