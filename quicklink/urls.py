"""quicklink URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import handler400, handler403, handler404, handler500  # @UnusedImport
from django.conf.urls import url, include
from django.contrib import admin

from . import views


urlpatterns = [
    url(r'^$',views.root), #redirect to actual root behind nginx
    url(r'^QuickLink/$', views.homepage),
    url(r'^QuickLink/envinfo/$', views.envinfo),
    url(r'^QuickLink/home/', include('home.urls')),
    url(r'^QuickLink/admin/', admin.site.urls),
]

handler400 = 'quicklink.views.bad_request'
handler403 = 'quicklink.views.permission_denied'
handler404 = 'quicklink.views.page_not_found'
handler500 = 'quicklink.views.server_error'