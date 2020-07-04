"""gms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from gmsapp.views import INBOXVIEW,NEWACCOUNTVIEW,MMVIEW,STVIEW
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^$',STVIEW),
    url(r'^admin/', admin.site.urls),
    url(r'^inbox/$', INBOXVIEW),
    url(r'^login/$',auth_views.login,{'template_name':'gmsapp/login.html'}),
    url(r'^logout/$',auth_views.logout_then_login),
    url(r'^newaccount/$',NEWACCOUNTVIEW),
    url(r'^send/$',MMVIEW),
]
