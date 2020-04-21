from django.shortcuts import HttpResponse
import json
from utils.pages import Pages

class BaseResponse(object):
    def __init__(self):
        self.status = True
        self.data = None
        self.message = None

class BaseDataService(object):
    def __init__(self):
        """
        mainData,                                   models.数据类
        condition_config.item{
            "name": "device_type",                  字段名称，用于数据库操作
            "caption": "设备类型",                  标题文字，用于界面显示
            "input_type": "select",                 输入类型：input/select
            "select_dict": "device_type_list",      当输入类型=select时，选择数据字典{k1:v1,k2:v2...}
        },
        table_config.item{
            "colname": "device_type",               字段名称，用于数据库操作
            "caption": "设备类型",                  标题文字，用于列表显示
            "display": {                            是否显示，0/1，不显示时，不需要设置edit和text
                "grid": 1,                          列表中
                "add": 1,                           新增时
                "detail": 1,                        详情中
            },
            "edit": {                               编辑属性
                "enable": 0,                        是否允许在列表直接编辑，0/1
                "type": "select",                   编辑时的输入类型，input/select
                "dict": "device_type_list",         当输入类型=select时，选择数据字典{k1:v1,k2:v2...}
            },
            "text": {
                "content": "设备{m}",                 文字显示格式，其中m是需要替换的参数
                "kwargs": {                             参数列表
                    "m": "@@device_type_list"           参数变量，@表示变量，@@表示根据当前行主键为key的字典
                },
                "align": "left",                        对齐方式
                "remark": ["备注信息1", "备注信息2"],   字段备注信息
            },
            "attr": {"kkk": "vvv"},                     需要添加的属性
            "group": "基础信息",                        字段分组信息，用于在detail、add等显示用
        },
        page_config.item{
            "baseUrl": "",                          页标签基础网址
            "onClick": ""                           当通过ajax请求页面时，需要使用onclick事件，这里填写对应函数名
        },
        global_dict.item{                           数据字典
            "key1": value1,
            "key2": value2
        },
        """
        self.mainData = None
        self.condition_config = []
        self.table_config = []
        self.page_config = {}
        self.global_dict = {}

    def getBaseList(self, request):
        response = BaseResponse()
        try:
            # 获取列表数据
            col_list = []
            for col in self.table_config:
                if col["colname"]:
                    col_list.append(col["colname"])
            queryCon = json.loads(request.GET.get("conditionDict", None))
            if len(queryCon) > 0:
                rs = self.mainData.objects.filter(**queryCon).values(*col_list)
            else:
                rs = self.mainData.objects.values(*col_list)
            # queryset不能json序列化，因此转换成列表
            rs = list(rs)

            # 分页
            cnt = request.COOKIES.get("reccnt_perpage")
            if not cnt:
                cnt = "10"
            if len(self.page_config["onClick"]) == 1:
                tmpFun = "$.initData"
            else:
                tmpFun = ""
            page = Pages(len(rs), int(cnt), self.page_config["jsonUrl"], self.page_config["newUrl"], request.GET.get("pageNum", 1), tmpFun)

            # 返回数据
            response.data = {
                "condition_config": self.condition_config,
                "table_config": self.table_config,
                "data_list": rs[page.startRec:page.endRec],
                "global_dict": self.global_dict,
                "page_info": {"page_str": page.pageStr, "startRec": page.startRec}
            }
        except Exception as e:
            response.status = False
            response.message = str(e)
        rep = HttpResponse(json.dumps(response.__dict__))
        rep.set_cookie("reccnt_perpage", cnt, path="/")
        return rep

    def getNew(self, request):
        response = BaseResponse()
        try:
            response.data = {
                "table_config": self.table_config,
                "global_dict": self.global_dict
            }
        except Exception as e:
            response.status = False
            response.message = str(e)
        rep = HttpResponse(json.dumps(response.__dict__))
        return rep

    def postData(self, request):
        response = BaseResponse()
        try:
            tmpDict = dict(request.POST)
            tmpDict.pop("csrfmiddlewaretoken")
            newDict = {}
            for key, value in tmpDict.items():
                newDict[key] = value[0]
            self.mainData.objects.create(**newDict)
        except Exception as e:
            response.status = False
            response.message = str(e)
        rep = HttpResponse(json.dumps(response.__dict__))
        return rep

    def putData(self, request):
        response = BaseResponse()
        try:
            from django.http import QueryDict
            PUT = QueryDict(request.body)
            updateDict = json.loads(PUT.get("updateDict", None))
            for key, value in updateDict.items():
                self.mainData.objects.filter(id=key).update(**value)
        except Exception as e:
            response.status = False
            response.message = str(e)
        rep = HttpResponse(json.dumps(response.__dict__))
        return rep

    def deleteData(self, request):
        response = BaseResponse()
        try:
            from django.http import QueryDict
            DELETE = QueryDict(request.body)
            deleteList = json.loads(DELETE.get("deleteList", None))
            for item in deleteList:
                self.mainData.objects.filter(id=item).delete()
        except Exception as e:
            response.status = False
            response.message = str(e)
        rep = HttpResponse(json.dumps(response.__dict__))
        return rep

    def getDetail(self, request):
        response = BaseResponse()
        try:
            nid = json.loads(request.GET.get("nid", None))
            # 获取列表数据
            col_list = []
            for col in self.table_config:
                if col["colname"]:
                    col_list.append(col["colname"])
            rec = self.mainData.objects.filter(id=nid).values(*col_list)
            rec = list(rec)[0]
            response.data = {
                "table_config": self.table_config,
                "data_detail": rec,
                "global_dict": self.global_dict
            }
        except Exception as e:
            response.status = False
            response.message = str(e)
        rep = HttpResponse(json.dumps(response.__dict__))
        return rep
