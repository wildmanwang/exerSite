from django.shortcuts import render, HttpResponse, redirect
from apps.business import models
from apps.baseinfo import models as base_models
from apps.sysmanager.views import auth
from django.forms import Form, fields, widgets
from django import forms
from django.core.exceptions import ValidationError
from utils.pages import Pages
import json
from datetime import date, datetime, timedelta

# Create your views here.


class FormRelEvent(Form):
    eventDate = fields.DateField(
        label="事件日期",
        widget=widgets.DateInput(attrs={"class": "inputType"}),
        required=False
    )
    eventName = fields.CharField(
        label="事件简称",
        max_length=50,
        widget=widgets.TextInput(attrs={"class": "inputType"}),
        required=False,
        error_messages={"max_length": "事件简称不能大于50位"}
    )
    family = forms.ModelChoiceField(
        label="家庭",
        widget=widgets.Select(attrs={"class": "inputType"}),
        queryset=base_models.Family.objects.all()
    )
    person = forms.ModelChoiceField(
        label="当事人",
        widget=widgets.Select(attrs={"class": "inputType"}),
        queryset=base_models.Person.objects.all(),
        required=False
    )
    eventType = fields.IntegerField(
        label="事件类型",
        widget=widgets.Select(choices=((None, "---------"), (1, "结婚"), (2, "生子"), (3, "周岁"), (4, "祝寿"), (5, "考学"), (6, "乔迁"), (7, "身故"), (99, "其他")), attrs={"class": "inputType"})
    )
    formType = fields.IntegerField(
        label="宴请类型",
        widget=widgets.Select(choices=((None, "---------"), (1, "隆重宴请"), (2, "亲朋小聚"), (3, "低调跳过"), (99, "待定")), attrs={"class": "inputType"})
    )
    eventDes = fields.CharField(
        label="事件说明",
        max_length=255,
        widget=widgets.TextInput(attrs={"class": "inputType"}),
        required=False,
        error_messages={"max_length": "事件简称不能大于255位"}
    )
    direction = fields.IntegerField(
        label="事件发起方",
        widget=widgets.RadioSelect(choices=((1, "我发起"), (2, "他人发起")))
    )
    dateFrom = fields.DateField(
        label="开始日期",
        widget=widgets.DateInput(attrs={"class": "inputType"}),
        required=False
    )
    dateTo = fields.DateField(
        label="截止日期",
        widget=widgets.DateInput(attrs={"class": "inputType"}),
        required=False
    )
    amtOutFood = fields.DecimalField(
        label="宴席支出金额",
        initial=0.00,
        min_value=0.00,
        max_value=9999999.99,
        max_digits=9,
        decimal_places=2,
        widget=widgets.NumberInput(attrs={"class": "inputType"})
    )
    amtOutOther = fields.DecimalField(
        label="其他支出金额",
        initial=0.00,
        min_value=0.00,
        max_value=9999999.99,
        max_digits=9,
        decimal_places=2,
        widget=widgets.NumberInput(attrs={"class": "inputType"})
    )
    cntFamily = fields.IntegerField(
        label="来宾户数",
        min_value=0,
        max_value=99999,
        widget=widgets.NumberInput(attrs={"class": "inputType"})
    )
    cntTable = fields.IntegerField(
        label="宴席桌数",
        min_value=0,
        max_value=99999,
        widget=widgets.NumberInput(attrs={"class": "inputType"})
    )
    amtInBook = fields.DecimalField(
        label="礼簿金额",
        initial=0.00,
        min_value=0.00,
        max_value=9999999.99,
        max_digits=9,
        decimal_places=2,
        widget=widgets.NumberInput(attrs={"class": "inputType"})
    )
    amtInOther = fields.DecimalField(
        label="其他收入金额",
        initial=0.00,
        min_value=0.00,
        max_value=9999999.99,
        max_digits=9,
        decimal_places=2,
        widget=widgets.NumberInput(attrs={"class": "inputType"})
    )
    status = fields.IntegerField(
        label="状态",
        widget=widgets.RadioSelect(choices=((1, "预测"), (2, "计划"), (9, "完成")))
    )
    remark = fields.CharField(
        label="备注",
        max_length=255,
        widget=widgets.TextInput(attrs={"class": "inputType"}),
        required=False,
        error_messages={"max_length": "备注不能大于255位"}
    )

    def clean_person(self):
        """
        字段校验：
        1 必须存在且只有一个“自己”
        2 “自己”必须已经设置了“家庭”
        :return:
        """
        data = self.cleaned_data["person"]
        rec = base_models.Person.objects.filter(id=data.id).first()
        if not rec:
            raise ValidationError(message="请选择当事人")
        if not rec.family:
            raise ValidationError(message="当事人必须先设置家庭")
        #other = base_models.Person.objects.filter(relType=0).first()
        #if rec.family != other.family:
        #    raise ValidationError(message="请选择当前家庭的成员")
        return data


class FormJoinRecordSpec(Form):
    joinFamily = forms.ModelChoiceField(
        label="出席家庭",
        widget=widgets.Select(attrs={"class": "selectSpc"}),
        queryset=base_models.Family.objects.filter(status=1)
    )
    amtBook = fields.DecimalField(
        label="礼金",
        initial=0.00,
        min_value=0.00,
        max_value=9999999.99,
        max_digits=9,
        decimal_places=2,
        widget=widgets.NumberInput(attrs={"class": "inputSpc"})
    )


class FormJoinRecord(Form):
    event = forms.ModelChoiceField(
        label="事件",
        widget=widgets.Select(attrs={"class": "inputType"}),
        queryset=models.RelEvent.objects.all(),
        required=False
    )
    joinFamily = forms.ModelChoiceField(
        label="出席家庭",
        widget=widgets.Select(attrs={"class": "inputType"}),
        queryset=base_models.Family.objects.filter(status=1)
    )
    amtBook = fields.DecimalField(
        label="礼金",
        initial=0.00,
        min_value=0.00,
        max_value=9999999.99,
        max_digits=9,
        decimal_places=2,
        widget=widgets.NumberInput(attrs={"class": "inputType"})
    )
    amtOther = fields.DecimalField(
        label="其他支出",
        initial=0.00,
        min_value=0.00,
        max_value=9999999.99,
        max_digits=9,
        decimal_places=2,
        widget=widgets.NumberInput(attrs={"class": "inputType"})
    )
    recTime = fields.DateTimeField(
        label="登记时间",
        widget=widgets.DateTimeInput(attrs={"class": "inputType"})
    )
    remark = fields.CharField(
        label="备注",
        max_length=255,
        widget=widgets.TextInput(attrs={"class": "inputType"}),
        required=False,
        error_messages={"max_length": "备注不能大于255位"}
    )


@auth
def relEventList(request, userID, status=0, pageNo=1):
    dateFrom = request.GET.get("from", None)
    dateTo = request.GET.get("to", None)
    status = int(status)
    if not dateFrom or not dateTo:
        if not dateFrom:
            dateFrom = date.today() - timedelta(days=31)
        if not dateTo:
            dateTo = date.today()
    else:
        dateFrom = datetime.strptime(dateFrom, "%Y-%m-%d")
        dateTo = datetime.strptime(dateTo, "%Y-%m-%d")
    if status != 1 and status != 2 and status != 9:
        dataList = models.RelEvent.objects.filter(user=userID, direction=1, eventDate__gte=dateFrom, eventDate__lte=dateTo)
    else:
        dataList = models.RelEvent.objects.filter(user=userID, direction=1, eventDate__gte=dateFrom, eventDate__lte=dateTo, status=status)
    cnt = request.COOKIES.get("reccnt_perpage")
    if not cnt:
        cnt = "10"
    page = Pages(len(dataList), int(cnt), "relEventList-%d-" % (status), pageNo)
    rep = render(request, "business/relEventList.html", {"dataList": dataList[page.startRec:page.endRec], "from": dateFrom, "to": dateTo, "pagetag": page.pageStr, "status": status, "recCnt": len(dataList)})
    rep.set_cookie("reccnt_perpage", cnt, path="/busi/")
    return rep


@auth
def relEventNew(request, userID):
    if request.method == "GET":
        rec = base_models.Person.objects.filter(user=userID, relType=0).first()
        dic = {
            "eventDate": date.today(),
            "family": rec.family,
            "direction": 1,
            "dateFrom": date.today(),
            "dateTo": date.today(),
            "amtInBook": 0.00,
            "amtInOther": 0.00,
            "status": 2
        }
        obj = FormRelEvent(initial=dic)
        return render(request, "business/relEventNew.html", {"form": obj})
    elif request.method == "POST":
        obj = FormRelEvent(request.POST)
        res = obj.is_valid()
        if res:
            obj.cleaned_data["user_id"] = userID
            models.RelEvent.objects.create(**obj.cleaned_data)
            return redirect("http://127.0.0.1:8000/busi/relEventList-0-1")
        else:
            return render(request, "business/relEventNew.html", {"form": obj})


@auth
def relEventDelete(request, userID, id):
    rtn = {
        "result": False,
        "data": None,
        "info": None
    }
    rec = models.RelEvent.objects.filter(id=id).first()
    if not rec:
        rtn["info"] = "查无此记录%d" % (id)
    else:
        rec.delete()
        rtn["result"] = True
    return HttpResponse(json.dumps(rtn))


@auth
def relEventModify(request, userID, id):
    if request.method == "GET":
        rec = models.RelEvent.objects.filter(id=id).first()
        dic = {
            "eventDate": rec.eventDate,
            "eventName": rec.eventName,
            "family": rec.family,
            "person": rec.person,
            "eventType": rec.eventType,
            "formType": rec.formType,
            "eventDes": rec.eventDes,
            "direction": rec.direction,
            "dateFrom": rec.dateFrom,
            "dateTo": rec.dateTo,
            "amtOutFood": rec.amtOutFood,
            "amtOutOther": rec.amtOutOther,
            "cntFamily": rec.cntFamily,
            "cntTable": rec.cntTable,
            "amtInBook": rec.amtInBook,
            "amtInOther": rec.amtInOther,
            "status": rec.status,
            "remark": rec.remark
        }
        obj = FormRelEvent(initial=dic)
        return render(request, "business/relEventModify.html", {"form": obj, "id": id})
    elif request.method == "POST":
        obj = FormRelEvent(request.POST)
        res = obj.is_valid()
        if res:
            models.RelEvent.objects.filter(id=id).update(**obj.cleaned_data)
            return redirect("http://127.0.0.1:8000/busi/relEventList-0-1")
        else:
            return render(request, "business/relEventModify.html", {"form": obj, "id": id})


@auth
def relEventDetail(request, userID, id):
    rec = models.RelEvent.objects.filter(id=id).first()
    obj = FormRelEvent()
    return render(request, "business/relEventDetail.html", {"form": obj, "rec": rec})


@auth
def relEventModifyBookList(request, userID, id, relType=0, pageNo=1):
    dicNumber = {1:0}
    recSum = 0
    dataList = []
    relType = int(relType)
    for i in [1,2,3,4,5,6,7,99]:
        dataList0 = models.JoinRecord.objects.filter(event=id, joinFamily__name__relType=i)
        dicNumber[i] = len(dataList0)
        recSum += len(dataList0)
        if relType == 0:
            if len(dataList0) > 0:
                dataList = dataList0
                relType = i
        elif relType == i:
            dataList = dataList0
    eventName = models.RelEvent.objects.filter(id=id).first().eventName
    cnt = request.COOKIES.get("reccnt_perpage")
    if not cnt:
        cnt = "10"
    page = Pages(len(dataList), int(cnt), "relEventModify-%s/bookList-" % (id), pageNo)
    rep = render(request, "business/relEventModifyBookList.html", {
        "dataList": dataList[page.startRec:page.endRec],
        "id": id,
        "eventName": eventName,
        "relNumber": dicNumber,
        "relType": relType,
        "pagetag": page.pageStr,
        "recCnt": recSum
    })
    rep.set_cookie("reccnt_perpage", cnt, path="/busi/relEventModify/")
    return rep


@auth
def relEventModifyBookNew(request, userID, id):
    event = models.RelEvent.objects.filter(id=id).first()
    if request.method == "GET":
        dic = {
            "event": models.RelEvent.objects.filter(id=id).first().id,
            "recTime": datetime.now()
        }
        obj = FormJoinRecordSpec(initial=dic)
        lastList = models.JoinRecord.objects.filter(event=event).order_by("-recTime")[:5]
        return render(request, "business/relEventModifyBookNew.html", {"form": obj, "id": id, "eventName": event.eventName, "lastList": lastList})
    elif request.method == "POST":
        obj = FormJoinRecordSpec(request.POST)
        res = obj.is_valid()
        if not res:
            return render(request, "business/relEventModifyBookNew.html", {"form": obj, "id": id, "eventName": event.eventName})
        obj.cleaned_data["user_id"] = userID
        obj.cleaned_data["event"] = event
        obj.cleaned_data["amtOther"] = 0.00
        obj.cleaned_data["recTime"] = datetime.now()
        obj.cleaned_data["remark"] = ""
        models.JoinRecord.objects.create(**obj.cleaned_data)
        return redirect("http://127.0.0.1:8000/busi/relEventModify/bookNew-%s" % (id))


@auth
def relEventModifyBookDelete(request, userID, subid):
    rtn = {
        "result": False,
        "data": None,
        "info": None
    }
    rec = models.JoinRecord.objects.filter(id=subid).first()
    if not rec:
        rtn["info"] = "查无此记录%d" % (id)
    else:
        rec.delete()
        rtn["result"] = True
    return HttpResponse(json.dumps(rtn))


@auth
def relEventModifyBookModify(request, userID, subid):
    rec = models.JoinRecord.objects.filter(id=subid).first()
    if request.method == "GET":
        dic = {
            "id": rec.id,
            "user_id": userID,
            "event": rec.event,
            "joinFamily": rec.joinFamily,
            "amtBook": rec.amtBook,
            "amtOther": rec.amtOther,
            "recTime": rec.recTime,
            "remark": rec.remark
        }
        obj = FormJoinRecord(initial=dic)
        return render(request, "business/relEventModifyBookModify.html", {"form": obj, "eventName": rec.event.eventName, "id": rec.event.id, "subid": subid})
    elif request.method == "POST":
        obj = FormJoinRecord(request.POST)
        res = obj.is_valid()
        if not res:
            return render(request, "business/relEventModifyBookModify.html", {"form": obj, "eventName": rec.event.eventName, "id": rec.event.id, "subid": subid})
        models.JoinRecord.objects.filter(id=subid).update(**obj.cleaned_data)
        return redirect("http://127.0.0.1:8000/busi/relEventModify/bookList-%d-0-1" % (rec.event.id))


@auth
def relEventModifyBookDetail(request, userID, subid):
    rec = models.JoinRecord.objects.filter(id=subid).first()
    obj = FormJoinRecord()
    return render(request, "business/relEventModifyBookDetail.html", {"form": obj, "rec": rec, "eventName": rec.event.eventName})


@auth
def joinRecordList(request, userID, pageNo=1):
    dateFrom = request.GET.get("from", None)
    dateTo = request.GET.get("to", None)
    eventType = request.COOKIES.get("joinRecordListEventType")
    formType = request.COOKIES.get("joinRecordListFormType")
    if not dateFrom or not dateTo:
        if not dateFrom:
            dateFrom = date.today() - timedelta(days=31)
        if not dateTo:
            dateTo = date.today()
    else:
        dateFrom = datetime.strptime(dateFrom, "%Y-%m-%d")
        dateTo = datetime.strptime(dateTo, "%Y-%m-%d")
    if not eventType or eventType == "0":
        if not formType or formType == "0":
            dataList = models.JoinRecord.objects.filter(user=userID, event__eventDate__gte=dateFrom, event__eventDate__lte=dateTo)
        else:
            dataList = models.JoinRecord.objects.filter(user=userID, event__eventDate__gte=dateFrom, event__eventDate__lte=dateTo, event__formType=int(formType))
    else:
        if not formType or formType == "0":
            dataList = models.JoinRecord.objects.filter(user=userID, event__eventDate__gte=dateFrom, event__eventDate__lte=dateTo, event__eventType=int(eventType))
        else:
            dataList = models.JoinRecord.objects.filter(user=userID, event__eventDate__gte=dateFrom, event__eventDate__lte=dateTo, event__eventType=int(eventType), event__formType=(int(formType)))
    cnt = request.COOKIES.get("reccnt_perpage")
    if not cnt:
        cnt = "10"
    page = Pages(len(dataList), int(cnt), "joinRecordList-", pageNo)
    rep = render(request, "business/joinRecordList.html", {"dataList": dataList[page.startRec:page.endRec], "from": dateFrom, "to": dateTo, "pagetag": page.pageStr, "recCnt": len(dataList)})
    rep.set_cookie("reccnt_perpage", cnt, path="/busi/")
    return rep


@auth
def joinRecordNew(request, userID):
    if request.method == "GET":
        dicEvent = {
            "eventDate": date.today(),
            "direction": 2,
            "dateFrom": date.today(),
            "dateTo": date.today(),
            "cntFamily": 0,
            "cntTable": 0,
            "status": 9
        }
        objEvent = FormRelEvent(initial=dicEvent)
        myFamily = base_models.Person.objects.filter(user=userID, relType=0).first().family
        dicRecord = {
            "joinFamily": myFamily,
            "recTime": datetime.now()
        }
        objRecord = FormJoinRecord(initial=dicRecord)
        return render(request, "business/joinRecordNew.html", {"formEvent": objEvent, "formRecord": objRecord})
    elif request.method == "POST":
        objEvent = FormRelEvent(request.POST)
        objRecord = FormJoinRecord(request.POST)
        res = objEvent.is_valid()
        if not res:
            return render(request, "business/joinRecordNew.html", {"formRecord": objRecord, "formEvent": objEvent})
        objEvent.cleaned_data["user_id"] = userID
        newEvent = models.RelEvent.objects.create(**objEvent.cleaned_data)
        res = objRecord.is_valid()
        if not res:
            return render(request, "business/joinRecordNew.html", {"formRecord": objRecord, "formEvent": objEvent})
        objRecord.cleaned_data["user_id"] = userID
        objRecord.cleaned_data["event"] = newEvent
        models.JoinRecord.objects.create(**objRecord.cleaned_data)
        return redirect("http://127.0.0.1:8000/busi/joinRecordList-1")


@auth
def joinRecordDelete(request, userID, id):
    rtn = {
        "result": False,
        "data": None,
        "info": None
    }
    rec = models.JoinRecord.objects.filter(id=id).first()
    if not rec:
        rtn["info"] = "查无此记录%d" % (id)
    else:
        rec.delete()
        rtn["result"] = True
    return HttpResponse(json.dumps(rtn))


@auth
def joinRecordModify(request, userID, id):
    if request.method == "GET":
        recRecord = models.JoinRecord.objects.filter(id=id).first()
        dicRecord = {
            "event": recRecord.event,
            "joinFamily": recRecord.joinFamily,
            "amtBook": recRecord.amtBook,
            "amtOther": recRecord.amtOther,
            "recTime": recRecord.recTime,
            "remark": recRecord.remark
        }
        objRecord = FormJoinRecord(initial=dicRecord)
        recEvent = models.RelEvent.objects.filter(id=recRecord.event.id).first()
        dicEvent = {
            "eventDate": recEvent.eventDate,
            "eventName": recEvent.eventName,
            "family": recEvent.family,
            "person": recEvent.person,
            "eventType": recEvent.eventType,
            "formType": recEvent.formType,
            "direction": recEvent.direction,
            "dateFrom": recEvent.dateFrom,
            "dateTo": recEvent.dateTo,
            "amtOutFood": recEvent.amtOutFood,
            "amtOutOther": recEvent.amtOutOther,
            "cntFamily": recEvent.cntFamily,
            "cntTable": recEvent.cntTable,
            "amtInBook": recEvent.amtInBook,
            "amtInOther": recEvent.amtInOther,
            "status": recEvent.status,
            "remark": recEvent.remark
        }
        objEvent = FormRelEvent(initial=dicEvent)
        return render(request, "business/joinRecordModify.html", {"formRecord": objRecord, "formEvent": objEvent, "id": id})
    elif request.method == "POST":
        objEvent = FormRelEvent(request.POST)
        objRecord = FormJoinRecord(request.POST)
        res = objRecord.is_valid()
        if not res:
            return render(request, "business/joinRecordModify.html", {"formRecord": objRecord, "formEvent": objEvent, "id": id})
        models.JoinRecord.objects.filter(id=id).update(**objRecord.cleaned_data)
        res = objEvent.is_valid()
        if not res:
            return render(request, "business/joinRecordModify.html", {"formRecord": objRecord, "formEvent": objEvent, "id": id})
        models.RelEvent.objects.filter(id=models.JoinRecord.objects.filter(id=id).first().event.id).update(**objEvent.cleaned_data)
        return redirect("http://127.0.0.1:8000/busi/joinRecordList-1")


@auth
def joinRecordDetail(request, userID, id):
    recRecord = models.JoinRecord.objects.filter(id=id).first()
    dicRecord = {
        "event": recRecord.event,
        "joinFamily": recRecord.joinFamily,
        "amtBook": recRecord.amtBook,
        "amtOther": recRecord.amtOther,
        "recTime": recRecord.recTime,
        "remark": recRecord.remark
    }
    objRecord = FormJoinRecord(initial=dicRecord)
    recEvent = models.RelEvent.objects.filter(id=recRecord.event.id).first()
    dicEvent = {
        "eventDate": recEvent.eventDate,
        "eventName": recEvent.eventName,
        "family": recEvent.family,
        "person": recEvent.person,
        "eventType": recEvent.eventType,
        "formType": recEvent.formType,
        "dateFrom": recEvent.dateFrom,
        "dateTo": recEvent.dateTo
    }
    objEvent = FormRelEvent(initial=dicEvent)
    return render(request, "business/joinRecordDetail.html", {"formRecord": objRecord, "recRecord": recRecord, "formEvent": objEvent, "recEvent": recEvent})
