from django.urls import path, re_path
from apps.business import views

urlpatterns = [
    re_path('relEventList-(?P<status>\d+)-(?P<pageNo>\d+)$', views.relEventList, name="eventList"),
    re_path('relEventNew$', views.relEventNew, name="eventNew"),
    re_path('relEventDelete-(?P<nid>\d+)$', views.relEventDelete, name="eventDelete"),
    re_path('relEventModify-(?P<nid>\d+)$', views.relEventModify, name="eventModify"),
    re_path('relEventModify/bookList-(?P<pid>\d+)-(?P<relType>\d+)-(?P<pageNo>\d+)$', views.relEventModifyBookList, name="bookList"),
    re_path('relEventModify/bookNew-(?P<pid>\d+)$', views.relEventModifyBookNew, name="bookNew"),
    re_path('relEventModify/bookDelete-(?P<subid>\d+)$', views.relEventModifyBookDelete, name="bookDelete"),
    re_path('relEventModify/bookModify-(?P<subid>\d+)$', views.relEventModifyBookModify, name="bookModify"),
    re_path('relEventModify/bookDetail-(?P<subid>\d+)$', views.relEventModifyBookDetail, name="bookDetail"),
    re_path('relEventDetail-(?P<nid>\d+)$', views.relEventDetail, name="eventDetail"),
    re_path('joinRecordList-(?P<pageNo>\d+)$', views.joinRecordList, name="joinList"),
    re_path('joinRecordNew$', views.joinRecordNew, name="joinNew"),
    re_path('joinRecordDelete-(?P<nid>\d+)$', views.joinRecordDelete, name="joinDelete"),
    re_path('joinRecordModify-(?P<nid>\d+)$', views.joinRecordModify, name="joinModify"),
    re_path('joinRecordDetail-(?P<nid>\d+)$', views.joinRecordDetail, name="joinDetail"),
]
