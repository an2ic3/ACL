from typing import Set

from django.core.files.storage import FileSystemStorage

from ..models import Service
from .proxy import ProxyService


class ACLFileService:
    _INCLUDES = ('10/8', '127/8', '172.16/12', '192.168/16')
    _EXCLUDES = ('all',)

    def __init__(self):
        self._fs = FileSystemStorage()
        self._proxy_service = ProxyService()

    def update_include_files(self, services: Set[Service]):
        for service in services:
            self._update_include_file(service)

        self._proxy_service.reload()

    def _update_include_file(self, service: Service):
        ips = frozenset(self._INCLUDES) | service.get_acl_ips()

        with self._fs.open(service.name, 'w') as f:
            for ip in ips:
                f.write(self._str_allow(ip))
            for ip in self._EXCLUDES:
                f.write(self._str_deny(ip))

    def _str_allow(self, ip: str):
        return f'allow {ip}\n'

    def _str_deny(self, ip: str):
        return f'deny {ip}\n'
