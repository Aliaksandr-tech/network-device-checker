from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .feature_defaults import DEFAULT_FEATURES
from django.utils import timezone

class Device(models.Model):
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    web_port = models.PositiveIntegerField(default=80, help_text="Порт веб-интерфейса (обычно 80 или 443)")

    last_login_status = models.BooleanField(null=True, blank=True, help_text="Статус последней проверки авторизации")
    last_login_checked = models.DateTimeField(null=True, blank=True, help_text="Время последней проверки авторизации")

    def __str__(self):
        return f"{self.manufacturer} {self.model}"

class Documentation(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    doc_type = models.CharField(choices=[("manual", "Manual"), ("datasheet", "Datasheet")], max_length=20)
    status = models.BooleanField(default=False)
    file_path = models.FileField(upload_to='docs/', max_length=255)

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

    def __str__(self):
        return f"{self.name} ({'✅' if self.supported else '❌'})"

@receiver(post_save, sender=Device)
def create_default_features(sender, instance, created, **kwargs):
    if created:
        for name in DEFAULT_FEATURES:
            Feature.objects.create(device=instance, name=name, supported=False)