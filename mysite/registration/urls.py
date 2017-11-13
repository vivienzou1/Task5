from django.conf.urls import url
from django.contrib.auth import views as auth_views
from registration import views


urlpatterns = [
    url(r'^register/$', views.register, name="register"),
    url(r'^login/$', auth_views.login,{'template_name':'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout_then_login, name="logout"),
    url(r'^confirmed/$', views.confirmed, name='confirmed'),
    url(r'^profile/(?P<user_name>.*)', views.profile, name="profile"),
]