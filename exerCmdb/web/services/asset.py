from django.http.request import QueryDict
from utils.pages import Pages
from utils.baseServer import BaseService
import json
from web.models import Asset


class ServiceAsset(BaseService):
    def __init__(self):
        super().__init__()

        self.condition_config = [
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
        self.table_config = [
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

    def getBaseList(self, request):
        # 获取列表数据
        col_list = []
        for col in self.table_config:
            if col["colname"]:
                col_list.append(col["colname"])
        queryCon = json.loads(request.GET.get("conditionDict", None))
        if len(queryCon) > 0:
            rs = Asset.objects.filter(**queryCon).values(*col_list)
        else:
            rs = Asset.objects.values(*col_list)
        # queryset不能json序列化，因此转换成列表
        rs = list(rs)

    def postData(self, request):
        pass

    def deleteData(self, request):
        pass
