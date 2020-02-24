from django.urls import path, re_path
from apps.baseinfo import views

urlpatterns = [
    re_path('personList-(?P<status>\d+)-(?P<pageNo>\d+)$', views.personList, name="personList"),
    re_path('personNew$', views.personNew, name="personNew"),
    re_path('personDelete-(?P<nid>\d+)$', views.personDelete, name="personDelete"),
    re_path('personModify-(?P<nid>\d+)$', views.personModify, name="personModify"),
    re_path('personDetail-(?P<nid>\d+)$', views.personDetail, name="personDetail"),
    re_path('familyList-(?P<status>\d+)-(?P<pageNo>\d+)$', views.familyList, name="familyList"),
    re_path('familyNew$', views.familyNew, name="familyNew"),
    re_path('familyDelete-(?P<nid>\d+)$', views.familyDelete, name="familyDelete"),
    re_path('familyModify-(?P<nid>\d+)$', views.familyModify, name="familyModify"),
    re_path('familyDetail-(?P<nid>\d+)$', views.familyDetail, name="familyDetail"),
]
