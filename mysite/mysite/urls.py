from django.conf.urls import url, include
<<<<<<< HEAD
from registration import views

=======
from myapp import views
from django.contrib.auth import views as auth_views
>>>>>>> c1a359054a872ff36a141f273673207d1c91f59a


urlpatterns = [
    url(r'^$', views.home),
<<<<<<< HEAD
    url(r'^', include('registration.urls')),
    #url(r'^account/', include('account.urls'))
=======
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, {'next_page': 'logged_out'}),
    url(r'^logged_out/$', views.logout_result, name='logged_out'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^accounts/profile/$', views.account, name='account'),
    url(r'^account/' , include('account.urls'))
>>>>>>> c1a359054a872ff36a141f273673207d1c91f59a
]