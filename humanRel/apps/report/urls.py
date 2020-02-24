from django.urls import path, re_path
from apps.report import views

urlpatterns = [
    re_path('repRelSum$', views.repRelSum, name="relSum"),
    re_path('repRelDetail$', views.repRelDetail, name="relDetail"),
    re_path('repRelForecast$', views.repRelForecast, name="relForecast"),
    re_path('repRelMap$', views.repRelMap, name="relMap"),
]
