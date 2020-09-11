from typing import Set

from django.core.files.storage import FileSystemStorage
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from ..models import Service, Group, User
from .proxy import ProxyService


class ACLFileService:
    _INCLUDES = ('10.0.0.0/8', '127.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16')
    _EXCLUDES = ('all',)

    def __init__(self):
        self._fs = FileSystemStorage()
        self._proxy_service = ProxyService()

    def update_include_files(self, services: Set[Service]):
        for service in services:
            self._update_include_file(service)
        self._reload_proxy()

    def _update_include_file(self, service: Service):
        ips = frozenset(self._INCLUDES) | service.get_acl_ips()

        with self._fs.open(service.name, 'w') as f:
            for ip in ips:
                if not ip:
                    continue
                f.write(self._str_allow(ip))
            for ip in self._EXCLUDES:
                f.write(self._str_deny(ip))

    def _str_allow(self, ip: str):
        return f'allow {ip};\n'

    def _str_deny(self, ip: str):
        return f'deny {ip};\n'

    def _reload_proxy(self):
        self._proxy_service.reload()

    def delete_service(self, service: Service):
        self._fs.delete(service.name)
        self._reload_proxy()


@receiver(post_delete, sender=Service)
def delete_service(sender, **kwargs):
    file_service = ACLFileService()
    file_service.delete_service(kwargs.get("instance"))
