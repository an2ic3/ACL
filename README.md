# ACL

A tool that can be used to create acces files for a nginx proxy.

## Env vars

* DB_DEFAULT_NAME: Name of the database
* DB_DEFAULT_USER: Name of the user of the database
* DB_DEFAULT_PASS: Password of the user
* DB_DEFAULT_HOST: Hostname or ip of the database server
* DB_DEFAULT_PORT: Port that is used to connect to the database
* DEBUG: enable or disable the debug settings
* ACL_FILE_PATH: Path to the folder where the include files are
* SCHEDULE_UPDATE_TIME: Time  for the schedule to iterate and request an ip for a domain
* PROXY_CONTAINER: Name of the container of the proxy
* LDAP_URI: URI to the LDAP-Server (ldap://localhost:1389)
* LDAP_BIND_DN: User for ldap search (cn=admin,dc=domain,dc=de)
* LDAP_BIND_PASS: Password of user(SECRET_PASSWORD)
* LDAP_USERS: OU of users(ou=people,dc=domain,dc=de)
* LDAP_GROUPS: OU of groups (ou=groups,dc=domain,dc=de)
* LDAP_USER: cn of user that allowed to use acl (cn=acl,ou=groups,dc=domain,dc=de)
* LDAP_SUPERUSER: con of superuser of acl (cn=superuser,cn=acl,ou=groups,dc=domain,dc=de)

## requirements

required is an postgres database