import base64
import binascii

from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.urls import reverse
from django.contrib.auth import authenticate


class BasicAuthMiddleware:
    _EXCLUDED_URLS = ('admin:index', )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        for url in self._EXCLUDED_URLS:
            if not request.path.startswith(reverse(url)):
                continue
            return self.get_response(request)

        try:
            if not (auth_header := request.headers.get('Authorization', None)):
                response = HttpResponse(status=401)
                response['WWW-Authenticate'] = 'Basic realm="ACL"'
                return response
            _, basic_auth = auth_header.split(' ')
            username, passwd = base64.b64decode(basic_auth).decode().split(':')
        except (ValueError, binascii.Error):
            return HttpResponseBadRequest()

        user = authenticate(request, username=username, password=passwd)
        if not user:
            return HttpResponse(status=401)

        request.user = user

        return self.get_response(request)
