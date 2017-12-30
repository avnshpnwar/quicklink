from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$',views.home),
    url(r'^recentsite/$', views.recentsite),
    url(r'^allsite/$', views.allsite),
    url(r'^modtable/$', views.modtable),
    url(r'^addsite/$', views.addsite),
    url(r'^editsite/$', views.editsite),
    url(r'^deletesite/$', views.deletesite),
    url(r'^batch/$', views.batchupload),
    url(r'^refresh/$', views.refresh),
    url(r'^success/$', views.successmsg, name='success'),
    url(r'^failure/$',views.failuremsg, name='failure'),
    url(r'^updaterecent/$',views.updaterecent),
    url(r'^help/$', views.helppage),
]
