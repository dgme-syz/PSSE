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
    # path('api/recognize_license_plate/', views.recognize_license_plate, name='recognize_license_plate'),
    path('api/add_car/', views.add_car, name='add_car'),
    path('api/park_car/', views.park_car, name='park_car'),
    path('api/delete_car/', views.delete_car, name='delete_car'),
    path('api/reset_parking_duration/', views.reset_parking_duration, name='reset_parking_duration'),
    path('api/update_parking_price/', views.update_parking_price, name='update_parking_price'),
    path('api/query_parking_record_by_date_day/', views.query_parking_record_by_date_day, name='query_parking_record_by_date'),
    path('api/get_parking_spots/', views.get_parking_spots, name='get_parking_spots'),
    path('api/get_csrf_token/', views.get_csrf_token, name='get_csrf_token'),
    path('api/unpaid_cars/', views.unpaid_cars, name='unpaid_cars'),
    path('api/monthly_income_api/', views.monthly_income_api, name='monthly_income_api'),
    path('api/daily_income_and_state_api/', views.daily_income_and_state_api, name='daily_income_and_state_api'),
    path('api/export_parking_data/', views.export_parking_data, name='export_parking_data'),

]
    
