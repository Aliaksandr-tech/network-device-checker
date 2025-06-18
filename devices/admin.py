from django.contrib import admin
from .models import Device, Documentation, AuthData, Feature

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('model', 'manufacturer', 'ip_address')
    search_fields = ('model', 'manufacturer')

@admin.register(Documentation)
class DocumentationAdmin(admin.ModelAdmin):
    list_display = ('device', 'doc_type', 'status')
    list_filter = ('doc_type', 'status')

@admin.register(AuthData)
class AuthDataAdmin(admin.ModelAdmin):
    list_display = ('device', 'access_type', 'login')

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('device', 'name', 'supported')
    list_filter = ('supported',)
    search_fields = ('name',)
