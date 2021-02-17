import ldap
import logging

from django.conf import settings

logger = logging.getLogger(__name__)


class LDAPService:

    def __init__(self, uid):
        self._uid = uid
        self._filter = f'(uid={uid})'
        self._server = ldap.initialize(settings.AUTH_LDAP_SERVER_URI)

    def _try_conn(self):
        try:
            self._server.protocol_version = ldap.VERSION3
            self._server.simple_bind_s(
                settings.AUTH_LDAP_BIND_DN,
                settings.AUTH_LDAP_BIND_PASSWORD
            )

            return True
        except ldap.INVALID_CREDENTIALS:
            logger.warning("Your username or password is incorrect.")
            return False
        except ldap.LDAPError as e:
            logger.error("LDAPError: %s", e)
            return False

    def close(self):
        self._server.unbind_s()

    def get_attr(self, key=[], *, default=None):
        if not self._try_conn():
            return

        ldap_result = None

        try:
            search_res = self._server.search_s(
                settings.AUTH_LDAP_USERS,
                ldap.SCOPE_SUBTREE,
                self._filter,
                [key]
            )

            _, ldap_result = search_res[0]
        except ldap.LDAPError as e:
            logger.error("LDAPError: %s", e)

        return ldap_result.get(key, default)

    def set_attr(self, key, value):
        if not self._try_conn():
            return

        try:
            self._server.modify_s(
                f'uid={self._uid},{settings.AUTH_LDAP_USERS}',
                [(ldap.MOD_REPLACE, key, value.encode())]
            )
        except ldap.LDAPError as e:
            logger.error("LDAPError: %s", e)
