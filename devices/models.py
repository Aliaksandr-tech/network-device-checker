from django.db import models

# Create your models here.
from django.db import models

class Device(models.Model):
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)

class Documentation(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    doc_type = models.CharField(choices=[("manual", "Manual"), ("datasheet", "Datasheet")], max_length=20)
    status = models.BooleanField(default=False)
    file_path = models.FileField(upload_to='docs/')

class AuthData(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    access_type = models.CharField(choices=[("web", "Web"), ("cli", "CLI")], max_length=10)
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

class Feature(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    supported = models.BooleanField()
    config_cli = models.TextField(null=True, blank=True)
    config_web = models.TextField(null=True, blank=True)
    doc_reference = models.CharField(max_length=200, null=True, blank=True)
