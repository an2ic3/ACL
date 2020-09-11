from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import User, Group
from django.db.models import Manager

from .models import IP, Service, Domain
from .service.acl_file import ACLFileService
from .service.dns_lookup import DNSLookupService


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    filter_horizontal = ('users', 'groups')

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        if not change:
            obj.save()
        for attr in form.changed_data:
            obj_attr = getattr(obj, attr)
            if issubclass(type(obj_attr), (BaseUserManager, Manager)):
                obj_attr.set(form.cleaned_data[attr])
            else:
                obj_attr = form.cleaned_data[attr]
        super().save_model(request, obj, form, change)

        if form.changed_data:
            file_service = ACLFileService()
            file_service.update_include_files({obj})


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

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        if not change:
            obj.save()
            return
        user_groups = [*obj.groups.all()]
        for attr in form.changed_data:
            obj_attr = getattr(obj, attr)
            if issubclass(type(obj_attr), (BaseUserManager, Manager)):
                obj_attr.set(form.cleaned_data[attr])
            else:
                obj_attr = form.cleaned_data[attr]
        super().save_model(request, obj, form, change)

        if form.changed_data:
            services = obj.ip.get_acl_services()
            if 'groups' in form.changed_data:
                user_groups += [*form.cleaned_data['groups']]
                services |= {*Service.objects.filter(groups__in=user_groups)}
            file_service = ACLFileService()
            file_service.update_include_files(services)

    def save_formset(self, request, form, formset, change):

        data = formset.cleaned_data[0]
        super().save_formset(request, form, formset, change)
        if formset.queryset.model == IP:
            return
        elif formset.queryset.model == Domain:
            dns_service = DNSLookupService()
            if not (user := data.get("user")):
                return
            if not (domain := data.get("domain")) or data.get("DELETE"):
                return
            if user.domain == domain:
                return
            ip = dns_service.look_up(domain)
            if ip == user.ip:
                return
            if ip:
                domain, created = Domain.objects.update_or_create(user=user, defaults={'domain': domain})

        else:
            file_service = ACLFileService()
            services = {data.get('service') or data.get('id').service
                        for data in formset.cleaned_data
                        if data.get('service') or data.get('id')}
            file_service.update_include_files(services)


class CustomGroupAdmin(GroupAdmin):
    pass
    # filter_horizontal = ('service',)
    # inlines = (
    #     GroupServiceInline,
    # )


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)
