from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('support/', include('support.urls')),
    path('accounts/', include('idm.urls')),
    path('', include('acl_manager.urls')),
]
