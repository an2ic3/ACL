from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group

from .models import IP, Service, Domain
from .service.acl_file import ACLFileService


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    filter_horizontal = ('users', 'groups')

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        for attr in form.changed_data:
            getattr(obj, attr).set(form.cleaned_data[attr])
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

    def save_formset(self, request, form, formset, change):
        data = formset.cleaned_data[0]
        super().save_formset(request, form, formset, change)

        if formset.queryset.model == IP:
            if data.get("id") and data.get("address") == data.get("id").address and not data.get("DELETE"):
                return
            if not (user := data.get("user")):
                return

            file_service = ACLFileService()
            services = user.ip.get_acl_services()

            file_service.update_include_files(services)


class CustomGroupAdmin(GroupAdmin):
    filter_horizontal = ('service',)
    inlines = (
        GroupServiceInline,
    )


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)
