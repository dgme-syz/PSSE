"""django_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from . import views

urlpatterns = [
    path('api/login/', views.user_login, name='login'),
    path('api/register/', views.register, name='register'),
    path('', views.home_view, name='home'),
    path('api/send_verification_code/', views.send_verification_code, name='send_verification_code'),
    path('api/change_password/', views.change_password, name='change_password'),
    path('api/change_email/', views.change_email, name='change_email')
]
