from django.urls import path, re_path
from apps.report import views

urlpatterns = [
    re_path('repRelSum$', views.repRelSum),
    re_path('repRelDetail$', views.repRelDetail),
    re_path('repRelForecast$', views.repRelForecast),
    re_path('repRelMap$', views.repRelMap),
]
