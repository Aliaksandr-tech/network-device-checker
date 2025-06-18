from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.device_search, name='device_search'),
    path('device/<int:device_id>/', views.device_detail, name='device_detail'),
    path('feature/<int:feature_id>/method/', views.feature_method_view, name='feature_method'),
    path('device/<int:device_id>/ping/', views.ping_device, name='ping_device'),
]