# Access Control List
A ip based forwarded authentication solution for traefik.

## Setup Instructions
* Build ACL
  ```bash
  $ sudo docker build -t acl app
  ```

* Export static files (you need to provide them using a nginx)
  ```bash
  $ sudo docker run --rm -u0 \
      -v '/srv/main/nginx/webroot/static.acl.example.com:/home/app/web/static' \
      --entrypoint='/home/app/web/manage.py'
      acl 'collectstatic --no-input'
  ```

* Modify [`docker-compose.yml`](./docker-compose.yml) (e.g. setting secure passwords, replacing `example` with your actual domain name and `com` with your actual top level domain)

* Start all services
  ```
  $ sudo docker-compose up -d
  ```

## Environment Variables

| Key                  | Description                                                                                                                       | Default Value                 |
|----------------------|-----------------------------------------------------------------------------------------------------------------------------------|-------------------------------|
| SQL_ENGINE           | Database Driver which should be used                                                                                              | django.db.backends.postgresql |
| SQL_HOST             | Hostname / IP of the database                                                                                                     |                               |
| SQL_PORT             | Database Port                                                                                                                     | 5432                          |
| SQL_USER             | Database User                                                                                                                     | acl                           |
| SQL_PASSWORD         | Database Password                                                                                                                 |                               |
| SQL_DATABASE         | Database Name                                                                                                                     | acl                           |
| SCHEDULE_UPDATE_TIME | time for the schedule to iterate and request an ip for a domain                                                                   | 15 (minutes)                  |
| DEBUG                | Debug Mode                                                                                                                        | 0 / False                     |
| SECRET_KEY           | Secret Key of the Django App                                                                                                      | [autogenerated]               |
| ALLOWED_HOSTS        |                                                                                                                                   | 0.0.0.0                       |
| STATIC_URL           |                                                                                                                                   | 0.0.0.0                       |
| LDAP_URI             | URI for ldap server - e.g. ldap://ldap:389 - if set ldap auth will be enabled                                                     |                               |
| LDAP_BIND_DN         | LDAP Bind DN - e.g. cn=admin,dc=example,dc=com                                                                                    |                               |
| LDAP_BIND_PASS       | LDAP Bind Password                                                                                                                |                               |
| LDAP_USERS           | LDAP Users / People OU - e.g. ou=people,dc=example,dc=com                                                                         |                               |
| LDAP_GROUPS          | LDAP Groups OU - e.g. ou=people,dc=example,dc=com                                                                                 |                               |
| LDAP_GROUP           | DN of LDAP Group, which users need to be member of to use the acl - e.g. cn=acl,ou=groups,dc=example,dc=com                       |                               |
| LDAP_SUPERGROUP      | DN of LDAP Group, which users need to be member of to administrate the acl - e.g. cn=superuser,cn=acl,ou=groups,dc=example,dc=com |                               |


## Simple Update
```bash
#!/bin/bash

IP=$(curl -q ifconfig.co 2> /dev/null)
USER="user"
API="acl.example.com"

read -sp "Password: " PASS
echo

one=$(curl "https://${USER}:${PASS}@${API}/update/?ip=1.1.1.1" 2> /dev/null)
if [ -z ${one} ]; then
  echo "Authentication failed!"
  exit 1
fi
current=$(curl "https://${USER}:${PASS}@${API}/update/?ip=${IP}" 2> /dev/null)
echo "${current} has been set for ${USER}@${API}"
```


## TODO
* (Paul) Improve LDAP search query to also enable login using common name / mail
  ```bash
  # hint
  (&(|(uid=%u))(|(mail=%u))(|(cn=%u)))
  # might work ... (something like this...)
  ```
* Remove unused environment variables (for the old nginx version of the acl)
* Add Identity Management (A page where the user can change his Password, Public Key and see in which groups he's in)
* Import LDAP Users on Basic Auth - not only on Admin Login