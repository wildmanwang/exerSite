from django.urls import re_path
from apps.backend import views

urlpatterns = [
    re_path('myblogs$', views.myblogs, name="myblogs"),
    re_path('set/user$', views.setUser, name="setUser"),
    re_path('set/acct$', views.setAcct, name="setAcct"),
    re_path('set/photo$', views.setPhoto, name="setPhoto"),
    re_path('set/blog$', views.setBlog, name="setBlog"),
]
