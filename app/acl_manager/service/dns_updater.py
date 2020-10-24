from django.core.validators import validate_ipv46_address
from django.core.exceptions import ValidationError

from ..models import Domain, User
from .dns_lookup import DNSLookupService


def update_ips():
    dns_service = DNSLookupService()
    users = User.objects.filter(domain__in=Domain.objects.all())

    for user in users:
        ip_address = dns_service.look_up(user.domain.domain)
        try:
            validate_ipv46_address(ip_address)
        except ValidationError:
            continue

        if ip_address == user.ip.address:
            continue

        user.ip.address = ip_address
        user.ip.save()
