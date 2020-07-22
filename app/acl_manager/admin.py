from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group

from .models import IP, Service, Domain


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    model = Service
    filter_horizontal = ('users', 'groups')


class IPInLine(admin.TabularInline):
    model = IP


class DomainInLine(admin.TabularInline):
    model = Domain


class UserServiceInline(admin.TabularInline):
    model = Service.users.through
    extra = 1


class GroupServiceInline(admin.TabularInline):
    model = Service.groups.through
    extra = 1


class CustomUserAdmin(UserAdmin):
    filter_horizontal = ('service', 'groups')
    inlines = (
        IPInLine,
        DomainInLine,
        UserServiceInline,
    )


class CustomGroupAdmin(GroupAdmin):
    pass
    filter_horizontal = ('service',)
    inlines = (
        GroupServiceInline,
    )


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)
