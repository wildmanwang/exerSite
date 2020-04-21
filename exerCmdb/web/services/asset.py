from utils.dataService import BaseDataService
from web import models


class ServiceAsset(BaseDataService):
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
                    "colname": "id",
                    "caption": "Id",
                    "display": {"grid": 0, "new": 0, "detail": 0},
                    "edit": {},
                    "text": {},
                    "attr": {},
                    "group": "基础信息",
                },
                {
                    "colname": "device_type_id",
                    "caption": "设备类型",
                    "display": {"grid": 1, "new": 1, "detail": 1},
                    "edit": {"enable": 0, "type": "select", "dict": "device_type_list", },
                    "text": {"content": "{m}", "kwargs": {"m": "@@device_type_list"}, "align": "left", "remark": ["设备简单分类", "不同的设备管理不同"],},
                    "attr": {"kkk": "vvv"},
                    "group": "",
                },
                {
                    "colname": "business_unit_id",
                    "caption": "业务线",
                    "display": {"grid": 1, "new": 1, "detail": 1},
                    "edit": {"enable": 1, "type": "select", "dict": "business_unit_list", },
                    "text": {"content": "{m}", "kwargs": {"m": "@@business_unit_list"}, "align": "left", "remark": ["公司主业分类", "主要用于资源调度"],},
                    "attr": {},
                    "group": "",
                },
                {
                    "colname": "idc_id",
                    "caption": "机房",
                    "display": {"grid": 1, "new": 1, "detail": 1},
                    "edit": {"enable": 1, "type": "select", "dict": "idc_list", },
                    "text": {"content": "{m}", "kwargs": {"m": "@@idc_list"}, "align": "left", "remark": ["设备当前所在机房", "物理位置"],},
                    "attr": {},
                    "group": "",
                },
                {
                    "colname": "cabinet_num",
                    "caption": "机柜号",
                    "display": {"grid": 1, "new": 1, "detail": 1},
                    "edit": {"enable": 1, "type": "input", },
                    "text": {"content": "{m}", "kwargs": {"m": "@cabinet_num"}, "align": "center", "remark": ["机房机柜", "机柜的编号"],},
                    "attr": {},
                    "group": "",
                },
                {
                    "colname": "cabinet_order",
                    "caption": "机柜中序号",
                    "display": {"grid": 1, "new": 1, "detail": 1},
                    "edit": {"enable": 1, "type": "input", },
                    "text": {"content": "{m}", "kwargs": {"m": "@cabinet_order"}, "align": "center", "remark": ["机柜中的序号", ""],},
                    "attr": {},
                    "group": "",
                },
                {
                    "colname": "employee_id",
                    "caption": "员工",
                    "display": {"grid": 1, "new": 1, "detail": 1},
                    "edit": {"enable": 1, "type": "select", "dict": "employee_list", },
                    "text": {"content": "{m}", "kwargs": {"m": "@@employee_list"}, "align": "left", "remark": ["当前使用方", ""],},
                    "attr": {},
                    "group": "其他信息",
                },
                {
                    "colname": "user_id",
                    "caption": "用户",
                    "display": {"grid": 1, "new": 1, "detail": 1},
                    "edit": {"enable": 1, "type": "select", "dict": "user_list", },
                    "text": {"content": "{m}", "kwargs": {"m": "@@user_list"}, "align": "left", "remark": ["运维登记方", ""],},
                    "attr": {},
                    "group": "",
                },
                {
                    "colname": "remark",
                    "caption": "备注",
                    "display": {"grid": 1, "new": 1, "detail": 1},
                    "edit": {"enable": 1, "type": "input", },
                    "text": {"content": "{m}", "kwargs": {"m": "@remark"}, "align": "left", "remark": ["", ""],},
                    "attr": {},
                    "group": "",
                },
                {
                    "colname": "device_status_id",
                    "caption": "设备状态",
                    "display": {"grid": 1, "new": 1, "detail": 1},
                    "edit": {"enable": 1, "type": "select", "dict": "device_status_list", },
                    "text": {"content": "{m}", "kwargs": {"m": "@@device_status_list"}, "align": "center", "remark": ["设备的当前状态", ""],},
                    "attr": {},
                    "group": "",
                },
                {
                    "colname": None,
                    "caption": "操作",
                    "display": {"grid": 1, "new": 0, "detail": 0},
                    "edit": {"enable": 0, },
                    "text": {"content": "<a href='/asset-detail-{m}.html'>查看详情</a>", "kwargs": {"m": "@id"}, "align": "center",},
                    "attr": {},
                    "group": "",
                }
            ]
        self.page_config = {
            "jsonUrl": "asset-json",
            "newUrl": "asset-new",
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
