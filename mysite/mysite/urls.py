from django.conf.urls import url, include
from registration import views
from django.contrib import admin
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home),
    url(r'^', include('registration.urls')),
    url(r'^log/', include('log.urls')),
    url(r'^account/', include('account.urls')),
<<<<<<< HEAD
    url(r'^loan/', include('loan.urls'))
=======
    url(r'^chat/', include('chat.urls'))
>>>>>>> 73889c62045604a9e9b4381c95cb4cee79962443
]