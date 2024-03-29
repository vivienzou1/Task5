from django.conf.urls import url
from django.contrib.auth import views as auth_views
from registration import views


urlpatterns = [
    url(r'^register/$', views.register, name="register"),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', auth_views.logout_then_login, name="logout"),
    url(r'^accounts/$', views.view_accounts, name='view_accounts'),
    url(r'^profile/$', views.profile, name="profile"),
    url(r'^base/$',views.base),
]