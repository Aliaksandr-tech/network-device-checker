from django.db import models
from django.contrib import admin
from .models import Feature

class Device(models.Model):
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.manufacturer} {self.model}"

class Documentation(models.Model):
    DOC_TYPES = [
        ("manual", "Manual"),
        ("datasheet", "Datasheet"),
    ]

    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    doc_type = models.CharField(max_length=20, choices=DOC_TYPES)
    status = models.BooleanField(default=False)
    file_path = models.FileField(upload_to='docs/')

    def __str__(self):
        return f"{self.doc_type} for {self.device}"

class AuthData(models.Model):
    ACCESS_TYPES = [
        ("web", "Web"),
        ("cli", "CLI"),
    ]

    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    access_type = models.CharField(max_length=10, choices=ACCESS_TYPES)
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.access_type} access for {self.device}"

class Feature(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    supported = models.BooleanField()
    config_cli = models.TextField(null=True, blank=True)
    config_web = models.TextField(null=True, blank=True)
    doc_reference = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({'Yes' if self.supported else 'No'})"


