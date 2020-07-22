from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import URLValidator


class IP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ip')
    address = models.GenericIPAddressField(protocol='both', blank=False, null=False)
    last_updated = models.DateTimeField(blank=False, null=False, default=timezone.now)

    def __str__(self):
        return self.address


class Service(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)

    def __str__(self):
        return self.name


class ACL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='acl')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="acl")

    def __str__(self):
        return self.service.name


class Domain(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='domain')
    domain = models.CharField(max_length=128, validators=[URLValidator])
    last_updated = models.DateTimeField(blank=False, null=False, default=timezone.now)

    def __str__(self):
        return self.domain
