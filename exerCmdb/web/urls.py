from django.urls import re_path
from web.views import asset, idc

urlpatterns = [
    re_path(r'asset$', asset.AssetView.as_view()),
    re_path(r'asset-json$', asset.AssetJsonView.as_view()),
    re_path(r'idc$', idc.IdcView.as_view()),
    re_path(r'idc-json$', idc.IdcJsonView.as_view()),
]
