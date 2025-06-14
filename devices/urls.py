from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.device_search, name='device_search'),
    path('device/<int:device_id>/', views.device_detail, name='device_detail'),
]
