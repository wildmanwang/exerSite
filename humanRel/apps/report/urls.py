from django.urls import path, re_path
from apps.report import views

urlpatterns = [
    re_path('repEventSum$', views.repEventSum),
    re_path('repEventDetail$', views.repEventDetail),
]
