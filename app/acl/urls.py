from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('acl_manager.urls')),
    path('support/', include('support.urls')),
]
