from django.urls import path, re_path
from apps.business import views

urlpatterns = [
    re_path('recEvent$', views.recEvent),
    re_path('recAttend$', views.recAttend),
]
