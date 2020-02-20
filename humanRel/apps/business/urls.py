from django.urls import path, re_path
from apps.business import views

urlpatterns = [
    re_path('relEventList-(?P<status>\d+)-(?P<pageNo>\d+)$', views.relEventList),
    re_path('relEventNew$', views.relEventNew),
    re_path('relEventDelete-(?P<id>\d+)$', views.relEventDelete),
    re_path('relEventModify-(?P<id>\d+)$', views.relEventModify),
    re_path('relEventModify/bookList-(?P<id>\d+)-(?P<relType>\d+)-(?P<pageNo>\d+)$', views.relEventModifyBookList),
    re_path('relEventModify/bookNew-(?P<id>\d+)$', views.relEventModifyBookNew),
    re_path('relEventModify/bookDelete-(?P<subid>\d+)$', views.relEventModifyBookDelete),
    re_path('relEventModify/bookModify-(?P<subid>\d+)$', views.relEventModifyBookModify),
    re_path('relEventModify/bookDetail-(?P<subid>\d+)$', views.relEventModifyBookDetail),
    re_path('relEventDetail-(?P<id>\d+)$', views.relEventDetail),
    re_path('joinRecordList-(?P<pageNo>\d+)$', views.joinRecordList),
    re_path('joinRecordNew$', views.joinRecordNew),
    re_path('joinRecordDelete-(?P<id>\d+)$', views.joinRecordDelete),
    re_path('joinRecordModify-(?P<id>\d+)$', views.joinRecordModify),
    re_path('joinRecordDetail-(?P<id>\d+)$', views.joinRecordDetail),
]
