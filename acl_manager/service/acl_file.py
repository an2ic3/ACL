from typing import List

from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User

from ..models import Service, IP, ACL


class ACLFileService:
    _INCLUDES = ('10/8', '127/8', '172.16/12', '192.168/16')
    _EXCLUDES = ('all',)

    def __init__(self):
        self._fs = FileSystemStorage()

    def update_include_files(self, services: List[Service]):
        for service in services:
            self._update_include_file(service)

    def _update_include_file(self, service: Service):
        ips = list(IP.objects.filter(user__acl__service=service).values_list('address', flat=True))
        ips.extend(self._INCLUDES)

        with self._fs.open(service.name, 'w') as f:
            for ip in ips:
                f.write(self._str_allow(ip))
            for ip in self._EXCLUDES:
                f.write(self._str_deny(ip))

    def _str_allow(self, ip: str):
        return f'allow {ip}\n'

    def _str_deny(self, ip: str):
        return f'deny {ip}\n'
