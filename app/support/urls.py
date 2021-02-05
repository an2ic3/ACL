from django.urls import path

from .views import index, edit, new, send_message


urlpatterns = [
    path('', index, name='support_index'),
    path('new/', new, name='support_new'),
    path('edit/<int:ticket_id>', edit, name='support_edit'),
    path('send/<int:ticket_id>', send_message, name='support_send_message')
]
