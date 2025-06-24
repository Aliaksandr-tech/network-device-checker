from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # шаблон стартовой
    path('search/', views.device_search, name='device_search'),
    path('device/<int:device_id>/', views.device_detail, name='device_detail'),
    path('feature/<int:feature_id>/method/', views.feature_method_view, name='feature_method'),
    path('device/<int:device_id>/ping/', views.ping_device, name='ping_device'),
    path('device/<int:device_id>/webcheck/', views.check_web, name='check_web'),
    path('device/<int:device_id>/extract-auth/', views.extract_auth_view, name='extract_auth'),



]