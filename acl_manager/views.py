from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, HttpResponseBadRequest
from django.views import View
from django.core.validators import validate_ipv46_address
from django.core.exceptions import ValidationError

from .models import IP, Service, Domain
from .service.acl_file import ACLFileService
from .service.dns_lookup import DNSLookupService


class InfoView(View):

    def get(self, request: HttpRequest, *args, **kwargs):
        try:
            ip_address = request.user.ip.address
        except IP.DoesNotExist:
            return HttpResponseNotFound()
        return HttpResponse(ip_address)


class UpdateView(View):

    def __init__(self):
        self._file_storage = ACLFileService()
        self._dns_service = DNSLookupService()

    def get(self, request: HttpRequest, *args, **kwargs):
        user = request.user

        if not (ip_address := request.GET.get('ip', None)):
            domain = request.GET.get('domain', None)
            ip_address = self._dns_service.look_up(domain)
            if ip_address:
                domain, created = Domain.objects.update_or_create(user=user, defaults={'domain': domain})
        else:
            Domain.objects.filter(user=user).delete()

        try:
            validate_ipv46_address(ip_address)
        except ValidationError:
            return HttpResponseBadRequest()

        ip, created = IP.objects.update_or_create(user=user, defaults={'address': ip_address})

        services = Service.objects.filter(acl__user=user)
        self._file_storage.update_include_files(services)

        return HttpResponse()
