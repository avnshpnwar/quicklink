from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$',views.logon),
    url(r'^logon/$', views.logon),
    url(r'^register/$', views.register),
    url(r'^changepwd/$', views.changepwd),
    url(r'^logout/$', views.userlogout),
]
