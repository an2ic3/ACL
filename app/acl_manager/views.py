from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseForbidden
from django.views import View
from django.core.validators import validate_ipv46_address
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import binascii
import base64

from .models import IP, Domain
from .service.dns_lookup import DNSLookupService


class InfoView(View):

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        try:
            ip_address = request.user.ip.address
        except IP.DoesNotExist:
            return HttpResponseNotFound()
        return HttpResponse(ip_address)


class UpdateView(View):

    def __init__(self):
        self._dns_service = DNSLookupService()

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not (ip_address := request.GET.get('ip')) and not (domain := request.GET.get('domain')):
            return HttpResponseBadRequest()

        user = request.user

        if ip_address:
            Domain.objects.filter(user=user).delete()
        elif ip_address := self._dns_service.look_up(domain):
            Domain.objects.update_or_create(user=user, defaults={'domain': domain})
        else:
            return HttpResponseBadRequest()

        try:
            validate_ipv46_address(ip_address)
        except ValidationError:
            return HttpResponseBadRequest()

        if hasattr(user, "ip"):
            if ip_address == user.ip.address:
                return HttpResponse(ip_address)

        IP.objects.update_or_create(user=user, defaults={'address': ip_address})

        return HttpResponse(ip_address)


class ACLAuthView(View):

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:

        if not (ip_header := request.headers.get("X-Forwarded-For")):
            return HttpResponseBadRequest()

        if not (host := request.headers.get("X-Forwarded-Host")):
            return HttpResponseBadRequest()

        if len(ip_header.split(",")) == 0:
            return HttpResponseBadRequest()

        ip_address, *_ = ip_header.split(",")

        try:
            validate_ipv46_address(ip_address)
        except ValidationError:
            return HttpResponseBadRequest()

        user_query_set = User.objects.filter(ip__address=ip_address)

        for user in user_query_set.all():
            if user.service.filter(name__iexact=host).exists():
                return HttpResponse()

        return HttpResponseForbidden()


class BasicAuthView(View):

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:

        if not (auth_header := request.headers.get('Authorization')):
            response = HttpResponse(status=401)
            response['WWW-Authenticate'] = 'Basic realm="ACL"'
            return response

        try:
            _, basic_auth = auth_header.split(' ')
            username, passwd = base64.b64decode(basic_auth).decode().split(':', maxsplit=1)
        except (ValueError, binascii.Error):
            return HttpResponseBadRequest()

        if authenticate(request, username=username, password=passwd):
            return HttpResponse()

        return HttpResponseForbidden()
