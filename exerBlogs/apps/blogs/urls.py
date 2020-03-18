from django.urls import re_path
from apps.blogs import views

urlpatterns = [
    re_path('', views.index, name="index"),
]
