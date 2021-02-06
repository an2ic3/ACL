from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('update/', views.UpdateView.as_view(), name='update'),
    path('check/', views.ACLAuthView.as_view(), name='auth'),
    path('checkauth/', views.BasicAuthView.as_view(), name='checkauth'),
]
