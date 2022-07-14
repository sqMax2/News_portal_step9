"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from newsapp.views import CeleryView, set_timezone

import logging


# logger_dr = logging.getLogger('django.request')
# logger_cn = logging.getLogger('django')
#
# logger_dr.error("Hello! I'm error in your app. Enjoy:)")
# logger_cn.error("Hello! I'm error in your app. Enjoy:)")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    # path('', include('django.contrib.flatpages.urls')),
    path('', include('protect.urls')),
    path('sign/', include('authapp.urls')),
    path('<slug:postType>/', include('newsapp.urls', namespace='newsapp')),
    path('accounts/', include('allauth.urls')),
    path('celery/', CeleryView.as_view(), name='celery'),
    # path('', set_timezone, name='set_timezone'),
]
