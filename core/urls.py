from django.urls import path
from . import views

urlpatterns = [
    path('', views.device_search_view, name='device_search'),
    path('device_autocomplete/', views.device_autocomplete, name='device_autocomplete'),
]
