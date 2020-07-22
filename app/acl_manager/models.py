from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.core.validators import URLValidator


class IP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ip')
    address = models.GenericIPAddressField(protocol='both', blank=False, null=False)
    last_updated = models.DateTimeField(blank=False, null=False, default=timezone.now)

    def __str__(self):
        return self.address

    def get_acl_services(self):
        return set(Service.objects.filter(users=self.user)) | set(
            Service.objects.filter(groups__in=self.user.groups.all())
        )


class Service(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)
    users = models.ManyToManyField(User, related_name="service", blank=True)
    groups = models.ManyToManyField(Group, related_name="service", blank=True)

    def __str__(self):
        return self.name

    def get_acl_ips(self):
        return set(self.users.values_list('ip__address', flat=True)) | set(
            User.objects.filter(groups__in=self.groups.all()).values_list('ip__address', flat=True)
        )


class Domain(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='domain')
    domain = models.CharField(max_length=128, validators=[URLValidator])
    last_updated = models.DateTimeField(blank=False, null=False, default=timezone.now)

    def __str__(self):
        return self.domain

    def get_acl_services(self):
        return set(Service.objects.filter(users=self.user)) | set(
            Service.objects.filter(groups__in=self.user.groups.all())
        )
