from django.shortcuts import render
from django.views import View
from web.services.idc import ServiceIdc


class IdcView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "idcList.html", {"pageTitle": "机房列表", "jsonUrl": "idc-json"})

class IdcJsonView(View):
    def get(self, request, *args, **kwargs):
        return ServiceIdc().getBaseList(request)

    def post(self, request, *args, **kwargs):
        return ServiceIdc().postData(request)

    def delete(self, request, *args, **kwargs):
        return ServiceIdc().deleteData(request)
