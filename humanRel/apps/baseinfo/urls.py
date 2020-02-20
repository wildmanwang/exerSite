from django.urls import path, re_path
from apps.baseinfo import views

urlpatterns = [
    re_path('personList-(?P<status>\d+)-(?P<pageNo>\d+)$', views.personList),
    re_path('personNew$', views.personNew),
    re_path('personDelete-(?P<id>\d+)$', views.personDelete),
    re_path('personModify-(?P<id>\d+)$', views.personModify),
    re_path('personDetail-(?P<id>\d+)$', views.personDetail),
    re_path('familyList-(?P<status>\d+)-(?P<pageNo>\d+)$', views.familyList),
    re_path('familyNew$', views.familyNew),
    re_path('familyDelete-(?P<id>\d+)$', views.familyDelete),
    re_path('familyModify-(?P<id>\d+)$', views.familyModify),
    re_path('familyDetail-(?P<id>\d+)$', views.familyDetail),
]
