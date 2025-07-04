from django.urls import path
from . import views
from .views import cli_auth_view

urlpatterns = [
    # path('', views.index, name='index'), # шаблон стартовой, # заглушка
    # path('search/', views.device_search, name='device_search'), # заглушка
    path('device/<int:device_id>/', views.device_detail, name='device_detail'),
    # path('feature/<int:feature_id>/method/', views.feature_method_view, name='feature_method'), # старый с заглушкой
    path('feature_method/<int:feature_id>/', views.feature_methodology_view, name='feature_method'), # новый
    path('device/<int:device_id>/ping/', views.ping_device, name='ping_device'),
    path('device/<int:device_id>/webcheck/', views.check_web, name='check_web'),
    path('device/<int:device_id>/extract-auth/', views.extract_auth_view, name='extract_auth'),
    path('device/<int:device_id>/weblogin/', views.web_login_view, name='web_login'),
    path('cli-auth/', views.cli_auth_view, name='cli-auth'),
    path('test/', views.test_view, name='test'), # временно для теста

    path('devices/<int:device_id>/check_datasheet/<int:feature_id>/', views.check_datasheet, name='check_datasheet'),
    path('devices/<int:device_id>/check_manual/<int:feature_id>/', views.check_manual_feature, name='check_manual_feature'),
    path('feature/<int:feature_id>/update_support/', views.update_feature_support, name='update_feature_support'),

]





