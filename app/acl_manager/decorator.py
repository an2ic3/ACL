import base64
import binascii
import logging

from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.contrib.auth import authenticate, login

logger = logging.getLogger(__name__)


def basic_auth_required(func):
    def wrapper(request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)

        if not (auth_header := request.headers.get('Authorization')):
            response = HttpResponse(status=401)
            response['WWW-Authenticate'] = 'Basic realm="ACL"'
            return response

        try:
            _, basic_auth = auth_header.split(' ')
            username, passwd = base64.b64decode(basic_auth).decode().split(':', maxsplit=1)
        except (ValueError, binascii.Error) as e:
            logger.error(e)
            return HttpResponseBadRequest()

        user = authenticate(request, username=username, password=passwd)
        if not user:
            return HttpResponse(status=401)

        login(request, user)

        return func(request, *args, **kwargs)
    return wrapper
