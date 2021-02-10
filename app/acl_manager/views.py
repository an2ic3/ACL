from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.core.validators import validate_ipv46_address
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from .decorator import basic_auth_required
from .models import IP, Domain
from .service.dns_lookup import DNSLookupService


def index(request):
    return redirect('profile')


class UpdateView(View):

    def __init__(self):
        self._dns_service = DNSLookupService()

    @method_decorator(basic_auth_required)
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
        if request.headers.get("Cf-Connecting-Ip"):
            ip_header = request.headers.get("Cf-Connecting-Ip")
        elif request.headers.get("X-Forwarded-For"):
            ip_header = request.headers.get("X-Forwarded-For")
        else:
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


# TODO add possibility to specify group
class BasicAuthView(LoginView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse()

        response = super(LoginView, self).get(request, *args, **kwargs)
        response.status_code = 401
        return response

    def post(self, *args, **kwargs):
        response = super().post(*args, **kwargs)

        if not isinstance(response, HttpResponseRedirect):
            return HttpResponseRedirect('/checkauth/')
        return HttpResponse()
