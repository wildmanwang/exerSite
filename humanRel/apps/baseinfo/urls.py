from django.urls import path, re_path
from apps.baseinfo import views

urlpatterns = [
    re_path('personList-(?P<status>\d+)-(?P<pageNo>\d+)$', views.personList),
    re_path('personNew$', views.personNew),
    re_path('personDelete-(?P<id>\d+)$', views.personDelete),
    re_path('personModify-(?P<id>\d+)$', views.personModify),
    re_path('personDetail-(?P<id>\d+)$', views.personDetail),
]
