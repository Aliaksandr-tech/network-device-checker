from django.contrib import admin
from .models import Device, Documentation, AuthData, Feature,FeatureMethodology

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('model', 'manufacturer', 'ip_address', 'web_port')
    list_filter = ('manufacturer',)
    search_fields = ('model', 'ip_address')

@admin.register(Documentation)
class DocumentationAdmin(admin.ModelAdmin):
    list_display = ('device', 'doc_type', 'status')
    list_filter = ('doc_type', 'status')

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        device_id = request.GET.get('device')
        if device_id:
            initial['device'] = device_id
        return initial


@admin.register(AuthData)
class AuthDataAdmin(admin.ModelAdmin):
    list_display = ('device', 'access_type', 'login')

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('device', 'name', 'supported')
    list_filter = ('supported',)
    search_fields = ('name',)

@admin.register(FeatureMethodology)
class FeatureMethodologyAdmin(admin.ModelAdmin):
    list_display = ('feature_name',)
    search_fields = ('feature_name',)