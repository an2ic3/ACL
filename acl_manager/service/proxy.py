import subprocess

from docker import from_env
from django.conf import settings


class ProxyService:

    def __init__(self):
        self._container = l[0] if (
            l := list(filter(lambda c: c.name == settings.PROXY_CONTAINER, from_env().containers.list()))
        ) else None

    def reload(self):
        if self._container:
            self._reload_container_proxy()
        else:
            self._reload_proxy()

    def _reload_container_proxy(self):
        self._container.exec_run('nginx -s reload')

    def _reload_proxy(self):
        subprocess.Popen(['/bin/sh', '-c', 'nginx -s reload'])
