"""OOAD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from django.urls import path,include
from django.conf.urls.static import static
from . import settings
from edit_online import views
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', views.index),
    path(r'index/', views.index),
    path(r'test1.pdf', views.printPDF),
    path(r'downloadPdf', views.downPDF),
    path(r'login/', views.login),
    path(r'register/', views.register),
    path(r'logout/', views.logout),
    path(r'captcha', include('captcha.urls'))
]
