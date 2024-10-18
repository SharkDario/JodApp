"""
URL configuration for jodapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
#from django.contrib.auth import views as auth_views
from moduloLogin.admin import admin_site
from modulo_ventas.views import ver_qr_pago
#from django.contrib.auth.views import LogoutView

urlpatterns = [
    #path("", admin.site.urls),
    path('', admin_site.urls),
    path('ver_qr_pago/<int:factura_id>/', ver_qr_pago, name='ver_qr_pago'),
]