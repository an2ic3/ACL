import base64
import binascii
import logging

from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.urls import reverse
from django.contrib.auth import authenticate


logger = logging.getLogger(__name__)


class BasicAuthMiddleware:
    _EXCLUDED_URLS = ('admin:index', 'auth')

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        for url in self._EXCLUDED_URLS:
            if not request.path.startswith(reverse(url)):
                continue
            return self.get_response(request)

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

        request.user = user

        return self.get_response(request)
