from django.shortcuts import render
from django.views import View
from web.services.asset import ServiceAsset


class AssetView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "assetList.html", {"pageTitle": "资产列表", "jsonUrl": "asset-json"})

class AssetJsonView(View):
    def get(self, request, *args, **kwargs):
        return ServiceAsset().getBaseList(request)

    def post(self, request, *args, **kwargs):
        return ServiceAsset().postData(request)

    def delete(self, request, *args, **kwargs):
        return ServiceAsset().deleteData(request)
