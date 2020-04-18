from utils.baseServer import BaseService
from web import models


class ServiceAsset(BaseService):
    def __init__(self):
        super().__init__()

        self.mainData = models.Asset

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
                    "select_dict": "device_type_list",
                },
                {
                    "name": "business_unit",
                    "caption": "业务线",
                    "input_type": "select",
                    "select_dict": "business_unit_list",
                },
                {
                    "name": "idc",
                    "caption": "机房",
                    "input_type": "select",
                    "select_dict": "idc_list",
                },
                {
                    "name": "cabinet_order",
                    "caption": "机柜中序号",
                    "input_type": "input",
                    "select_dict": "",
                },
                {
                    "name": "employee",
                    "caption": "员工",
                    "input_type": "select",
                    "select_dict": "employee_list",
                },
                {
                    "name": "user",
                    "caption": "用户",
                    "input_type": "select",
                    "select_dict": "user_list",
                },
                {
                    "name": "device_status_id",
                    "caption": "设备状态",
                    "input_type": "select",
                    "select_dict": "device_status_list",
                }
            ]
        self.table_config = [
                {
                    "colname": "id",        # 对应数据库列名
                    "caption": "Id",        # 显示的标题
                    "display": 0,           # 是否显示该列
                    "edit": {},             # {"enable": 0, "type": "input", "dict": "", }编辑选项
                    "text": {},             # {"content": "{m}", "kwargs": {"m": "@device_type"}, "align": "center",}，@表示用数据列代入， @@表示使用数据字典
                    "attr": {},             # {"key1": "value2", "key2": "@column"}，@表示用数据列代入
                },
                {
                    "colname": "device_type",
                    "caption": "设备类型",
                    "display": 1,
                    "edit": {"enable": 0, "type": "select", "dict": "device_type_list", },
                    "text": {"content": "{m}", "kwargs": {"m": "@@device_type_list"}, "align": "left",},
                    "attr": {"kkk": "vvv"},
                },
                {
                    "colname": "business_unit",
                    "caption": "业务线",
                    "display": 1,
                    "edit": {"enable": 1, "type": "select", "dict": "business_unit_list", },
                    "text": {"content": "{m}", "kwargs": {"m": "@@business_unit_list"}, "align": "left",},
                    "attr": {},
                },
                {
                    "colname": "idc",
                    "caption": "机房",
                    "display": 1,
                    "edit": {"enable": 1, "type": "select", "dict": "idc_list", },
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
                    "edit": {"enable": 1, "type": "select", "dict": "employee_list", },
                    "text": {"content": "{m}", "kwargs": {"m": "@@employee_list"}, "align": "left",},
                    "attr": {},
                },
                {
                    "colname": "user",
                    "caption": "用户",
                    "display": 1,
                    "edit": {"enable": 1, "type": "select", "dict": "user_list", },
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
                    "edit": {"enable": 1, "type": "select", "dict": "device_status_list", },
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

        self.page_config = {
            "baseUrl": "asset-json",
            "onClick": "1"
        }

        # 初始化数据字典
        self.global_dict = {}
        self.global_dict["device_status_list"] = {1: "上架", 2: "上线", 3: "离线", 4: "下架", }
        dict_rs = list(models.AssetType.objects.values("id", "name"))
        self.global_dict["device_type_list"] = dict(zip([item["id"] for item in dict_rs], [item["name"] for item in dict_rs]))
        dict_rs = list(models.BusinessUnit.objects.values("id", "name"))
        self.global_dict["business_unit_list"] = dict(zip([item["id"] for item in dict_rs], [item["name"] for item in dict_rs]))
        dict_rs = list(models.Idc.objects.values("id", "name", "floor"))
        self.global_dict["idc_list"] = dict(zip([item["id"] for item in dict_rs], [str(item["floor"]) + "楼-" + item["name"] for item in dict_rs]))
        dict_rs = list(models.EmployeeInfo.objects.values("id", "name"))
        self.global_dict["employee_list"] = dict(zip([item["id"] for item in dict_rs], [item["name"] for item in dict_rs]))
        dict_rs = list(models.UserInfo.objects.values("id", "username"))
        self.global_dict["user_list"] = dict(zip([item["id"] for item in dict_rs], [item["username"] for item in dict_rs]))
