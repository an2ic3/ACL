from django.core.validators import validate_ipv46_address
from django.core.exceptions import ValidationError

from ..models import Domain, User
from .dns_lookup import DNSLookupService
from .acl_file import ACLFileService


def update_ips():
    file_service = ACLFileService()
    dns_service = DNSLookupService()
    users = User.objects.filter(domain__in=Domain.objects.all())
    services = set()

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
        services |= user.domain.get_acl_services()

    if services:
        file_service.update_include_files(services)
