from utils.baseServer import BaseService
from web import models


class ServiceIdc(BaseService):
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
                    "colname": "id",        # 对应数据库列名
                    "caption": "Id",        # 显示的标题
                    "display": 0,           # 是否显示该列
                    "edit": {},             # {"enable": 0, "type": "input", "dict": "", }编辑选项
                    "text": {},             # {"content": "{m}", "kwargs": {"m": "@device_type"}, "align": "center",}，@表示用数据列代入， @@表示使用数据字典
                    "attr": {},             # {"key1": "value2", "key2": "@column"}，@表示用数据列代入
                },
                {
                    "colname": "name",
                    "caption": "名称",
                    "display": 1,
                    "edit": {"enable": 1, "type": "input", "dict": "", },
                    "text": {"content": "{m}", "kwargs": {"m": "@name"}, "align": "left",},
                    "attr": {"kkk": "vvv"},
                },
                {
                    "colname": "floor",
                    "caption": "楼层",
                    "display": 1,
                    "edit": {"enable": 1, "type": "input", "dict": "", },
                    "text": {"content": "{m}", "kwargs": {"m": "@floor"}, "align": "right",},
                    "attr": {},
                },
                {
                    "colname": None,
                    "caption": "操作",
                    "display": 1,
                    "edit": {"enable": 0, },
                    "text": {"content": "<a href='/idc-detail-{m}.html'>查看详情</a>", "kwargs": {"m": "@id"}, "align": "center", },
                    "attr": {},
                }
            ]

        self.page_config = {
            "baseUrl": "idc-json",
            "onClick": "1"
        }

        # 初始化数据字典
        self.global_dict = {}
