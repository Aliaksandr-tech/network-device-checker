from django.urls import path
from . import views

urlpatterns = [
    path('', views.device_search_view, name='device_search'),
    # потом добавим detail
]
