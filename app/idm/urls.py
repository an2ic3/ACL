from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.LoginView.as_view(),  name='login'),
    path('profile/', views.profile, name='profile'),
    path('updatePassword/', views.update_password, name='change_password'),
    path('updatePubkey/', views.update_pubkey, name='change_pubkey'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
