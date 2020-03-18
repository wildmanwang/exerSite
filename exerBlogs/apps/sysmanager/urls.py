from django.urls import re_path
from apps.sysmanager import views

urlpatterns = [
    re_path('login$', views.login, name="login"),
    re_path('logout$', views.logout, name="logout"),
    re_path('register$', views.register, name="register"),
]
