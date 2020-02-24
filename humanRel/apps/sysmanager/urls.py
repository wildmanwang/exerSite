from django.urls import path, re_path
from apps.sysmanager import views

urlpatterns = [
    re_path('register$', views.register, name="register"),
    re_path('login/', views.login, name="login"),
    re_path('logout', views.logout, name="logout"),
    re_path('index$', views.index, name="index"),
    re_path('set$', views.set, name="set"),
]
