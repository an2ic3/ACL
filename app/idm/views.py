import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, redirect

from .forms import ChangePasswordForm, ChangeSshPublicKeyForm
from acl_manager.models import Service, IP

from .service import LDAPService


def index(request):
    return redirect('profile')


class LoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def post(self, *args, **kwargs):
        response = super().post(*args, **kwargs)

        if not isinstance(response, HttpResponseRedirect):
            return HttpResponse(status=401)
        return response


@login_required
def profile(request):

    data = {
        'current_ip': None,
        'authorized_ip': None,
        'acl_authorization': [],
        'ldap_member_of': [],
        'givenName': None,
        'sn': None,
        'changePasswordForm': ChangePasswordForm(),
        'changeSshPublicKeyForm': None,
    }

    # get current ip address of the user
    # Cf-Connecting-Ip if your application is behind a Cloudflare proxies,
    # X-Forwarded-For if your application is behind a normal reverse proxy (like traefik)
    # REMOTE_ADDR from the meta information if the application is directly connected
    if request.headers.get("Cf-Connecting-Ip"):
        ip_header = request.headers.get("Cf-Connecting-Ip")
    elif request.headers.get("X-Forwarded-For"):
        ip_header = request.headers.get("X-Forwarded-For")
    else:
        ip_header = request.META.get('REMOTE_ADDR')

    if ip_header and len(ip_header.split(",")) > 0:
        data['current_ip'], *_ = ip_header.split(",")

    try:
        data['authorized_ip'] = request.user.ip.address
    except IP.DoesNotExist:
        pass

    data['acl_authorization'] = Service.objects.filter(
        Q(users=request.user) | Q(groups__in=request.user.groups.all())
    ).all()

    service = LDAPService(request.user.username)

    data['ldap_member_of'] = [s.decode() for s in service.get_attr('memberOf', default=[])]
    data['givenName'] = service.get_attr('givenName')[0].decode()
    data['sn'] = service.get_attr('sn')[0].decode()

    public_key_form = ChangeSshPublicKeyForm()
    public_key_form.fields['public_key'].initial = service.get_attr('sshPublicKey')[0].decode()
    data['changeSshPublicKeyForm'] = public_key_form

    service.close()

    return render(request, 'profile.html', context=data)


def update_password(request):
    data = json.loads(request.body)
    if 'password' not in data:
        return HttpResponseBadRequest()

    service = LDAPService(request.user.username)
    service.set_attr('userPassword', data.get('password'))
    service.close()

    return HttpResponse()


def update_pubkey(request):
    data = json.loads(request.body)
    if 'public_key' not in data:
        return HttpResponseBadRequest()

    service = LDAPService(request.user.username)
    service.set_attr('sshPublicKey', data.get('public_key'))
    service.close()

    return HttpResponse()
