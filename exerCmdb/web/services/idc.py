from utils.dataService import BaseDataService
from web import models


class ServiceIdc(BaseDataService):
    def __init__(self):
        super().__init__()

        self.mainData = models.Idc
        self.condition_config = [
                {
                    "name": "name",
                    "caption": "名称",
                    "input_type": "input",
                },
                {
                    "name": "floor",
                    "caption": "楼层",
                    "input_type": "input",
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
                    "colname": "name",
                    "caption": "名称",
                    "display": {"grid": 1, "new": 1, "detail": 1},
                    "edit": {"enable": 1, "type": "input", "dict": "", },
                    "text": {"content": "{m}", "kwargs": {"m": "@name"}, "align": "left", "remark": ["备注信息1", "备注信息2"],},
                    "attr": {"kkk": "vvv"},
                    "group": "",
                },
                {
                    "colname": "floor",
                    "caption": "楼层",
                    "display": {"grid": 1, "new": 1, "detail": 1},
                    "edit": {"enable": 1, "type": "input", "dict": "", },
                    "text": {"content": "{m}", "kwargs": {"m": "@floor"}, "align": "right", "remark": ["备注信息1", "备注信息2"],},
                    "attr": {},
                    "group": "",
                },
                {
                    "colname": None,
                    "caption": "操作",
                    "display": {"grid": 1, "new": 0, "detail": 0},
                    "edit": {"enable": 0, },
                    "text": {"content": "<a href='/idc-detail-{m}.html'>查看详情</a>", "kwargs": {"m": "@id"}, "align": "center", },
                    "attr": {},
                    "group": "",
                }
            ]
        self.page_config = {
            "jsonUrl": "idc-json",
            "newUrl": "idc-new",
            "onClick": "1"
        }

        self.global_dict = {}
