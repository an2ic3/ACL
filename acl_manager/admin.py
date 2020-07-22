from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import IP, ACL, Service, Domain


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass


class IPInLine(admin.TabularInline):
    model = IP


class DomainInLine(admin.TabularInline):
    model = Domain


class ACLInLine(admin.TabularInline):
    model = ACL
    extra = 1


class CustomUserAdmin(UserAdmin):

    inlines = (
        IPInLine,
        DomainInLine,
        ACLInLine,
    )


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
