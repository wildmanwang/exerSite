from django.shortcuts import render
from django.views import View
from web.services.asset import ServiceAsset


class AssetView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "assetList.html", {"pageTitle": "资产列表", "jsonUrl": "asset-json", "newUrl": "asset-new"})


class AssetJsonView(View):
    def get(self, request, *args, **kwargs):
        return ServiceAsset().getBaseList(request)

    def put(self, request, *args, **kwargs):
        return ServiceAsset().putData(request)

    def delete(self, request, *args, **kwargs):
        return ServiceAsset().deleteData(request)


class AssetDetailView(View):
    def get(self, request, nid, *args, **kwargs):
        return render(request, "assetDetail.html", {"pageTitle": "资产详情", "jsonUrl": "asset-detail-json", "baseUrl": "asset", "nid": nid})


class AssetDetailJsonView(View):
    def get(self, request, *args, **kwargs):
        return ServiceAsset().getDetail(request)


class AssetNewView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "assetNew.html", {"pageTitle": "新增资产", "jsonUrl": "asset-new-json", "baseUrl": "asset"})


class AssetNewJsonView(View):
    def get(self, request, *args, **kwargs):
        return ServiceAsset().getNew(request)

    def post(self, request, *args, **kwargs):
        return ServiceAsset().postData(request)
