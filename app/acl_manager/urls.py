from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views


urlpatterns = [
    path('', views.InfoView.as_view(), name='info'),
    path('update/', views.UpdateView.as_view(), name='update'),
    path('check/', views.ACLAuthView.as_view(), name='auth'),
    path('checkauth/', views.BasicAuthView.as_view(), name='checkauth'),
    path('accounts/login/', views.LoginView.as_view(),  name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
]
