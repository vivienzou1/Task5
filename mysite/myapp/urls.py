from django.conf.urls import url, include
from myapp import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, {'next_page': 'logged_out'}),
    url(r'^logged_out/$', views.logout_result, name='logged_out'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^accounts/profile/$', views.account, name='account'),
]