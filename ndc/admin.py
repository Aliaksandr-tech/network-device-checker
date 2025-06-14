from django.contrib import admin
from .models import Device, Documentation, AuthData, Feature

admin.site.register(Device)
admin.site.register(Documentation)
admin.site.register(AuthData)
admin.site.register(Feature)
