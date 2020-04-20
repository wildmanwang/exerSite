from django.urls import re_path
from web.views import asset, idc

urlpatterns = [
    re_path(r'asset$', asset.AssetView.as_view(), name='asset'),
    re_path(r'asset-json$', asset.AssetJsonView.as_view()),
    re_path(r'asset-detail-(?P<nid>\d+)', asset.AssetDetailView.as_view()),
    re_path(r'asset-detail-json', asset.AssetDetailJsonView.as_view()),
    re_path(r'asset-new$', asset.AssetNewView.as_view(), name='asset-new'),
    re_path(r'asset-new-json$', asset.AssetNewJsonView.as_view()),

    re_path(r'idc$', idc.IdcView.as_view(), name='idc'),
    re_path(r'idc-json$', idc.IdcJsonView.as_view()),
    re_path(r'idc-detail-(?P<nid>\d+)', idc.IdcDetailView.as_view()),
    re_path(r'idc-detail-json', idc.IdcDetailJsonView.as_view()),
    re_path(r'idc-new', idc.IdcNewView.as_view(), name='idc-new'),
    re_path(r'idc-new-json', idc.IdcNewJsonView.as_view()),
]
