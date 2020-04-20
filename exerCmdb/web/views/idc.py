from django.shortcuts import render
from django.views import View
from web.services.idc import ServiceIdc


class IdcView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "idcList.html", {"pageTitle": "机房列表", "jsonUrl": "idc-json", "newUrl": "idc-new"})


class IdcJsonView(View):
    def get(self, request, *args, **kwargs):
        return ServiceIdc().getBaseList(request)

    def put(self, request, *args, **kwargs):
        return ServiceIdc().putData(request)

    def delete(self, request, *args, **kwargs):
        return ServiceIdc().deleteData(request)


class IdcDetailView(View):
    def get(self, request, nid, *args, **kwargs):
        return render(request, "idcDetail.html", {"pageTitle": "机房详情", "jsonUrl": "idc-detail-json", "nid": nid})


class IdcDetailJsonView(View):
    def get(self, request, *args, **kwargs):
        return ServiceIdc().getDetail(request)


class IdcNewView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "idcNew.html", {"pageTitle": "新增机房", "jsonUrl": "idc-new-json"})

    def post(self, request, *args, **kwargs):
        return ServiceIdc().postData(request)


class IdcNewJsonView(View):
    def get(self, request, *args, **kwargs):
        return ServiceIdc().getNew(request)
