from django.shortcuts import render, HttpResponse
from django.views import View
from web import models
from utils.baseServer import BaseResponse
from utils.pages import Pages
import json


class AssetView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "assetList.html", {"pageTitle": "资产列表"})

class AssetJsonView(View):
    def get(self, request, *args, **kwargs):
        response = BaseResponse()
        try:
            # 获取查询条件
            condition_config = [
                {
                    "name": "cabinet_num",
                    "caption": "机柜号",
                    "input_type": "input",
                },
                {
                    "name": "device_type",
                    "caption": "设备类型",
                    "input_type": "select",
                    "data_source": "device_type_list",
                },
                {
                    "name": "business_unit",
                    "caption": "业务线",
                    "input_type": "select",
                    "data_source": "business_unit_list",
                },
                {
                    "name": "idc",
                    "caption": "机房",
                    "input_type": "select",
                    "data_source": "idc_list",
                },
                {
                    "name": "cabinet_order",
                    "caption": "机柜中序号",
                    "input_type": "input",
                    "data_source": "",
                },
                {
                    "name": "employee",
                    "caption": "员工",
                    "input_type": "select",
                    "data_source": "employee_list",
                },
                {
                    "name": "user",
                    "caption": "用户",
                    "input_type": "select",
                    "data_source": "user_list",
                },
                {
                    "name": "device_status_id",
                    "caption": "设备状态",
                    "input_type": "select",
                    "data_source": "device_status_list",
                }
            ]

            # 获取表头
            table_config = [
                {
                    "colname": "id",        # 对应数据库列名
                    "caption": "Id",        # 显示的标题
                    "display": 0,           # 是否显示该列
                    "edit": {},             # {"enable": 0, "type": "input", "dataDict": "", }编辑选项
                    "text": {},             # {"content": "{m}", "kwargs": {"m": "@device_type"}, "align": "center",}，@表示用数据列代入， @@表示使用数据字典
                    "attr": {},             # {"key1": "value2", "key2": "@column"}，@表示用数据列代入
                },
                {
                    "colname": "device_type",
                    "caption": "设备类型",
                    "display": 1,
                    "edit": {"enable": 0, "type": "select", "dataDict": "device_type_list", },
                    "text": {"content": "{m}", "kwargs": {"m": "@@device_type_list"}, "align": "left",},
                    "attr": {"kkk": "vvv"},
                },
                {
                    "colname": "business_unit",
                    "caption": "业务线",
                    "display": 1,
                    "edit": {"enable": 1, "type": "select", "dataDict": "business_unit_list", },
                    "text": {"content": "{m}", "kwargs": {"m": "@@business_unit_list"}, "align": "left",},
                    "attr": {},
                },
                {
                    "colname": "idc",
                    "caption": "机房",
                    "display": 1,
                    "edit": {"enable": 1, "type": "select", "dataDict": "idc_list", },
                    "text": {"content": "{m}", "kwargs": {"m": "@@idc_list"}, "align": "left",},
                    "attr": {},
                },
                {
                    "colname": "cabinet_num",
                    "caption": "机柜号",
                    "display": 1,
                    "edit": {"enable": 1, "type": "input", },
                    "text": {"content": "{m}", "kwargs": {"m": "@cabinet_num"}, "align": "center",},
                    "attr": {},
                },
                {
                    "colname": "cabinet_order",
                    "caption": "机柜中序号",
                    "display": 1,
                    "edit": {"enable": 1, "type": "input", },
                    "text": {"content": "{m}", "kwargs": {"m": "@cabinet_order"}, "align": "center",},
                    "attr": {},
                },
                {
                    "colname": "employee",
                    "caption": "员工",
                    "display": 1,
                    "edit": {"enable": 1, "type": "select", "dataDict": "employee_list", },
                    "text": {"content": "{m}", "kwargs": {"m": "@@employee_list"}, "align": "left",},
                    "attr": {},
                },
                {
                    "colname": "user",
                    "caption": "用户",
                    "display": 1,
                    "edit": {"enable": 1, "type": "select", "dataDict": "user_list", },
                    "text": {"content": "{m}", "kwargs": {"m": "@@user_list"}, "align": "left",},
                    "attr": {},
                },
                {
                    "colname": "remark",
                    "caption": "备注",
                    "display": 1,
                    "edit": {"enable": 1, "type": "input", },
                    "text": {"content": "{m}", "kwargs": {"m": "@remark"}, "align": "left",},
                    "attr": {},
                },
                {
                    "colname": "device_status_id",
                    "caption": "设备状态",
                    "display": 1,
                    "edit": {"enable": 1, "type": "select", "dataDict": "device_status_list", },
                    "text": {"content": "{m}", "kwargs": {"m": "@@device_status_list"}, "align": "center",},
                    "attr": {},
                },
                {
                    "colname": None,
                    "caption": "操作",
                    "display": 1,
                    "edit": {"enable": 0, },
                    "text": {"content": "<a href='/asset-detail-{m}.html'>查看详情</a>", "kwargs": {"m": "@id"}, "align": "center",},
                    "attr": {},
                }
            ]

            # 获取列表数据
            col_list = []
            for col in table_config:
                if col["colname"]:
                    col_list.append(col["colname"])
            queryCon = json.loads(request.GET.get("conditionDict", None))
            if len(queryCon) > 0:
                rs = models.Asset.objects.filter(**queryCon).values(*col_list)
            else:
                rs = models.Asset.objects.values(*col_list)
            # queryset不能json序列化，因此转换成列表
            rs = list(rs)

            # 分页
            cnt = request.COOKIES.get("reccnt_perpage")
            if not cnt:
                cnt = "10"
            page = Pages(len(rs), int(cnt), "asset-json", request.GET.get("pageNum", 1), "$.initData")

            # 初始化数据字典
            global_dict = {
                "device_status_list": { 1: "上架", 2: "上线", 3: "离线", 4: "下架", },
            }
            dict_rs = list(models.AssetType.objects.values("id", "name"))
            global_dict["device_type_list"] = dict(zip([item["id"] for item in dict_rs], [item["name"] for item in dict_rs]))
            dict_rs = list(models.BusinessUnit.objects.values("id", "name"))
            global_dict["business_unit_list"] = dict(zip([item["id"] for item in dict_rs], [item["name"] for item in dict_rs]))
            dict_rs = list(models.Idc.objects.values("id", "name", "floor"))
            global_dict["idc_list"] = dict(zip([item["id"] for item in dict_rs], [str(item["floor"]) + "楼-" + item["name"] for item in dict_rs]))
            dict_rs = list(models.EmployeeInfo.objects.values("id", "name"))
            global_dict["employee_list"] = dict(zip([item["id"] for item in dict_rs], [item["name"] for item in dict_rs]))
            dict_rs = list(models.UserInfo.objects.values("id", "username"))
            global_dict["user_list"] = dict(zip([item["id"] for item in dict_rs], [item["username"] for item in dict_rs]))

            # 返回数据
            response.data = {
                "condition_config": condition_config,
                "table_config": table_config,
                "data_list": rs[page.startRec:page.endRec],
                "global_dict": global_dict,
                "page_info": {"page_str": page.pageStr, "startRec": page.startRec}
            }
        except Exception as e:
            response.status = False
            response.message = str(e)
        rep = HttpResponse(json.dumps(response.__dict__))
        rep.set_cookie("reccnt_perpage", cnt, path="/")
        return rep

    def post(self, request, *args, **kwargs):
        response = BaseResponse()
        try:
            updateDict = json.loads(request.POST.get("updateDict", None))
            for key, value in updateDict.items():
                models.Asset.objects.filter(id=key).update(**value)
        except Exception as e:
            response.status = False
            response.message = str(e)
        rep = HttpResponse(json.dumps(response.__dict__))
        return rep

    def delete(self, request, *args, **kwargs):
        response = BaseResponse()
        try:
            from django.http import QueryDict
            PUT = QueryDict(request.body)
            deleteList = json.loads(PUT.get("deleteList", None))
            for item in deleteList:
                models.Asset.objects.filter(id=item).delete()
        except Exception as e:
            response.status = False
            response.message = str(e)
        rep = HttpResponse(json.dumps(response.__dict__))
        return rep
