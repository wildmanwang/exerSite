from django.shortcuts import render, HttpResponse, redirect, reverse
from apps.baseinfo import models
from apps.sysmanager.models import User
from apps.sysmanager.views import auth
from django.forms import Form, fields, widgets
from django import forms
from django.core.exceptions import ValidationError
from utils.pages import Pages
import json

# Create your views here.


class FormPerson(Form):
    # 唯一“自己”校验需要用到id、user，需要在模板form中提交，页面又不需要输入，因此required=False
    id = fields.IntegerField(
        label="ID",
        widget=widgets.TextInput(attrs={"class": "inputType"}),
        required=False,
        help_text=["", ""]
    )
    user = forms.ModelChoiceField(
        label="USER",
        widget=widgets.Select(attrs={"class": "inputType"}),
        queryset=User.objects.filter(status=1),
        required=False,
        help_text=["", ""]
    )
    name = fields.CharField(
        label="姓名",
        max_length=50,
        widget=widgets.TextInput(attrs={"class": "inputType"}),
        error_messages={"max_length": "姓名长度不能大于50"},
        help_text=["请填写真实姓名", "以便人员识别"]
    )
    gender = fields.IntegerField(
        label="性别",
        widget=widgets.RadioSelect(choices=((0, "女"), (1, "男")), attrs={"class": "inputOther"}),
        help_text=["用于婚姻", "以及根据地方习俗预测生日祝寿"]
    )
    birthDate = fields.DateField(
        label="出生日期",
        widget=widgets.DateInput(attrs={"class": "inputType"}),
        required=False,
        help_text=["用于计算年龄", "预测生日等"]
    )
    relType = fields.IntegerField(
        label="关系类型",
        widget=widgets.Select(choices=((None, "---------"), (0, "自己"), (1, "族亲"), (2, "姻亲"), (3, "同学"), (4, "朋友"), (5, "同事"), (6, "战友"), (7, "街坊"), (99, "其他")), attrs={"class": "inputType"}),
        help_text=["关系类型", "可用于查询和统计分类"]
    )
    family = forms.ModelChoiceField(
        label="家庭",
        widget=widgets.Select(attrs={"class": "inputType"}),
        queryset=models.Family.objects.filter(status=1),
        required=False,
        help_text=["关联户主", "人情往来都是以家庭为单位"]
    )
    father = forms.ModelChoiceField(
        label="父亲",
        widget=widgets.Select(attrs={"class": "inputType"}),
        queryset=models.Person.objects.filter(gender=1, Marriage=1, status=1),
        required=False,
        help_text=["用于建立父子关系", "以及关联父系亲属"]
    )
    mother = forms.ModelChoiceField(
        label="母亲",
        widget=widgets.Select(attrs={"class": "inputType"}),
        queryset=models.Person.objects.filter(gender=0, Marriage=1, status=1),
        required=False,
        help_text=["用于建立母子关系", "以及关联母系亲属"]
    )
    Marriage = fields.IntegerField(
        label="婚姻状态",
        widget=widgets.RadioSelect(choices=((0, "未婚"), (1, "已婚")), attrs={"class": "inputOther"}),
        help_text=["用于关联配偶", "以及预测结婚生子"]
    )
    spouse = forms.ModelChoiceField(
        label="配偶",
        widget=widgets.Select(attrs={"class": "inputType"}),
        queryset=models.Person.objects.filter(status=1),
        required=False,
        help_text=["用于建立夫妻关系", "以及关联姻亲"]
    )
    mobile = fields.CharField(
        label="手机号码",
        min_length=11,
        max_length=11,
        validators=[fields.validators.RegexValidator("^1[345678]\d{9}$", message="手机号码格式不正确")],
        widget=widgets.TextInput(attrs={"class": "inputType"}),
        required=False,
        help_text=["主要的联系方式", "请务必填写真实信息"]
    )
    weixin = fields.CharField(
        label="微信号",
        max_length=50,
        widget=widgets.TextInput(attrs={"class": "inputType"}),
        required=False,
        error_messages={"max_length": "微信号码不能大于50位"},
        help_text=["请填写微信号码", "默认为手机号"]
    )
    email = fields.EmailField(
        label="电子邮箱",
        max_length=255,
        widget=widgets.EmailInput(attrs={"class": "inputType"}),
        required=False,
        error_messages={"max_length": "电子邮箱不能大于255位"},
        help_text=["请填写电子邮箱地址", ""]
    )
    address = fields.CharField(
        label="现住址",
        max_length=255,
        widget=widgets.TextInput(attrs={"class": "inputType"}),
        required=False,
        error_messages={"max_length": "现住址不能大于255位"},
        help_text=["请填写当前居住地址", ""]
    )
    workUnit = fields.CharField(
        label="工作单位",
        max_length=50,
        widget=widgets.TextInput(attrs={"class": "inputType"}),
        required=False,
        error_messages={"max_length": "工作单位不能大于50位"},
        help_text=["请填写工作单位", ""]
    )
    education = fields.IntegerField(
        label="学历",
        widget=widgets.Select(choices=((None, "---------"), (0, "在读"), (1, "小学"), (2, "初中"), (3, "高中"), (4, "大专"), (5, "本科"), (6, "硕士"), (7, "博士"), (99, "其他")), attrs={"class": "inputType"}),
        help_text=["请选择学历", "在教育的学生将自动更新学历"]
    )
    occupation = fields.CharField(
        label="职业",
        max_length=20,
        widget=widgets.TextInput(attrs={"class": "inputType"}),
        required=False,
        error_messages={"max_length": "职业不能大于20位"},
        help_text=["请填写职业", ""]
    )
    status = fields.IntegerField(
        label="状态",
        initial=1,
        widget=widgets.RadioSelect(choices=((0, "失效"), (1, "正常"))),
        help_text=["人员状态", "不再联系的人可以设置失效"]
    )
    remark = fields.CharField(
        label="备注",
        max_length=255,
        widget=widgets.TextInput(attrs={"class": "inputType"}),
        required=False,
        error_messages={"max_length": "备注不能大于255位"},
        help_text=["其他信息", ""]
    )

    def __init__(self, userID, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["family"].queryset = models.Family.objects.filter(user_id=userID, status=1)
        self.fields["father"].queryset = models.Person.objects.filter(user_id=userID, gender=1, Marriage=1, status=1)
        self.fields["mother"].queryset = models.Person.objects.filter(user_id=userID, gender=0, Marriage=1, status=1)
        self.fields["spouse"].queryset = models.Person.objects.filter(user_id=userID, status=1)

    def clean(self):
        """
        字段校验：
        1 关系类型只能设置一个“自己”
        :return:
        """
        data = self.cleaned_data["relType"]
        if data == 0:
            personID = self.cleaned_data["id"]
            user = self.cleaned_data["user"].id
            if not personID:
                # 新增
                queryRst = models.Person.objects.filter(user=user, relType=0, status=1).first()
                if queryRst:
                    raise ValidationError(message="【{name}】已定义为“自己”，不能定义多个自己".format(name=queryRst.name))
                else:
                    return self.cleaned_data
            else:
                # 修改
                queryRst = models.Person.objects.filter(user=user, relType=0, status=1).exclude(id=personID).first()
                if queryRst:
                    raise ValidationError(message="【{name}】已定义为“自己”，不能定义多个自己".format(name=queryRst.name))
                else:
                    return self.cleaned_data
        else:
            return self.cleaned_data


class FormFamily(Form):
    name = forms.ModelChoiceField(
        label="姓名",
        widget=widgets.Select(attrs={"class": "inputType"}),
        queryset=models.Person.objects.filter(status=1),
        help_text=["请填写真实姓名", "以便人员识别"]
    )
    location = fields.CharField(
        label="所在城市/村镇",
        max_length=50,
        widget=widgets.TextInput(attrs={"class": "inputType"}),
        required=False,
        error_messages={"max_length": "所在城市/村镇不能大于50位"},
        help_text=["请填写所在城市或者村", "用于地域分类"]
    )
    address = fields.CharField(
        label="家庭住址",
        max_length=255,
        widget=widgets.TextInput(attrs={"class": "inputType"}),
        required=False,
        error_messages={"max_length": "家庭住址不能大于255位"},
        help_text=["请填写家庭详细住址", "各家庭成员共用"]
    )
    status = fields.IntegerField(
        label="状态",
        initial=1,
        widget=widgets.RadioSelect(choices=((0, "失效"), (1, "正常"))),
        help_text=["正常状态才能被选择", "才能新增事件"]
    )
    remark = fields.CharField(
        label="备注",
        max_length=255,
        widget=widgets.TextInput(attrs={"class": "inputType"}),
        required=False,
        error_messages={"max_length": "备注不能大于255位"},
        help_text=["其他信息", ""]
    )


@auth
def personList(request, userID, status=9, pageNo=1):
    status = int(status)
    if status != 0 and status != 1:
        dataList = models.Person.objects.filter(user=userID)
    else:
        dataList = models.Person.objects.filter(user=userID, status=status)
    cnt = request.COOKIES.get("reccnt_perpage")
    if not cnt:
        cnt = "10"
    page = Pages(len(dataList), int(cnt), "personList-%d-" % (status), pageNo)
    rep = render(request, "baseinfo/personList.html", {"dataList": dataList[page.startRec:page.endRec], "pagetag": page.pageStr, "status": status})
    rep.set_cookie("reccnt_perpage", cnt, path="/base/")
    return rep


@auth
def personNew(request, userID):
    if request.method == "GET":
        user = User.objects.filter(id=userID).first()
        dic = {
            "user": user
        }
        obj = FormPerson(initial=dic, userID=userID)
        return render(request, "baseinfo/personNew.html", {"form": obj, "user_id": userID})
    elif request.method == "POST":
        obj = FormPerson(userID=userID, data=request.POST)
        res = obj.is_valid()
        if not res:
            return render(request, "baseinfo/personNew.html", {"form": obj})
        obj.cleaned_data["user_id"] = userID
        models.Person.objects.create(**obj.cleaned_data)
        return redirect(reverse("app-base:personList", args=(1, 1, )))


@auth
def personDelete(request, userID, nid):
    rtn = {
        "result": False,
        "data": None,
        "info": None
    }
    rec = models.Person.objects.filter(id=nid).first()
    if not rec:
        rtn["info"] = "查无此记录%d" % (nid)
    else:
        rec.delete()
        rtn["result"] = True
    return HttpResponse(json.dumps(rtn))


@auth
def personModify(request, userID, nid):
    if request.method == "GET":
        rec = models.Person.objects.filter(id=nid).first()
        dic = {
            "id": rec.id,
            "user": rec.user,
            "name": rec.name,
            "gender": rec.gender,
            "birthDate": rec.birthDate,
            "relType": rec.relType,
            "family": rec.family,
            "father": rec.father,
            "mother": rec.mother,
            "Marriage": rec.Marriage,
            "spouse": rec.spouse,
            "mobile": rec.mobile,
            "weixin": rec.weixin,
            "email": rec.email,
            "address": rec.address,
            "workUnit": rec.workUnit,
            "education": rec.education,
            "occupation": rec.occupation,
            "status": rec.status,
            "remark": rec.remark
        }
        obj = FormPerson(initial=dic, userID=userID)
        return render(request, "baseinfo/personModify.html", {"form": obj, "nid": nid})
    elif request.method == "POST":
        obj = FormPerson(userID=userID, data=request.POST)
        res = obj.is_valid()
        if not res:
            return render(request, "baseinfo/personModify.html", {"form": obj, "nid": nid})
        models.Person.objects.filter(id=nid).update(**obj.cleaned_data)
        return redirect(reverse("app-base:personList", args=(1, 1, )))


@auth
def personDetail(request, userID, nid):
    rec = models.Person.objects.filter(id=nid).first()
    dic = {
        "id": rec.id,
        "user_id": userID,
        "name": rec.name,
        "gender": rec.gender,
        "birthDate": rec.birthDate,
        "relType": rec.relType,
        "family": rec.family,
        "father": rec.father,
        "mother": rec.mother,
        "Marriage": rec.Marriage,
        "spouse": rec.spouse,
        "mobile": rec.mobile,
        "weixin": rec.weixin,
        "email": rec.email,
        "address": rec.address,
        "workUnit": rec.workUnit,
        "education": rec.education,
        "occupation": rec.occupation,
        "status": rec.status,
        "remark": rec.remark
    }
    obj = FormPerson(initial=dic, userID=userID)
    return render(request, "baseinfo/personDetail.html", {"form": obj, "rec": rec})


@auth
def familyList(request, userID, status=9, pageNo=1):
    status = int(status)
    if status != 0 and status != 1:
        dataList = models.Family.objects.filter(user=userID)
    else:
        dataList = models.Family.objects.filter(user=userID, status=status)
    cnt = request.COOKIES.get("reccnt_perpage")
    if not cnt:
        cnt = "10"
    page = Pages(len(dataList), int(cnt), "familyList-%d-" % (status), pageNo)
    rep = render(request, "baseinfo/familyList.html", {"dataList": dataList[page.startRec:page.endRec], "pagetag": page.pageStr, "status": status})
    rep.set_cookie("reccnt_perpage", cnt, path="/base/")
    return rep


@auth
def familyNew(request, userID):
    if request.method == "GET":
        dic = {
            "status": 1
        }
        obj = FormFamily(initial=dic)
        return render(request, "baseinfo/familyNew.html", {"form": obj})
    elif request.method == "POST":
        obj = FormFamily(data=request.POST)
        res = obj.is_valid()
        if res:
            obj.cleaned_data["user_id"] = userID
            models.Family.objects.create(**obj.cleaned_data)
            return redirect(reverse("app-base:familyList", args=(1, 1, )))
        else:
            return render(request, "baseinfo/familyNew.html", {"form": obj})


@auth
def familyDelete(request, userID, nid):
    rtn = {
        "result": False,
        "data": None,
        "info": None
    }
    rec = models.Family.objects.filter(id=nid).first()
    if not rec:
        rtn["info"] = "查无此记录%d" % (nid)
    else:
        rec.delete()
        rtn["result"] = True
    return HttpResponse(json.dumps(rtn))


@auth
def familyModify(request, userID, nid):
    if request.method == "GET":
        rec = models.Family.objects.filter(id=nid).first()
        dic = {
            "name": rec.name,
            "location": rec.location,
            "address": rec.address,
            "status": rec.status,
            "remark": rec.remark
        }
        obj = FormFamily(initial=dic)
        return render(request, "baseinfo/familyModify.html", {"form": obj, "nid": nid})
    elif request.method == "POST":
        obj = FormFamily(data=request.POST)
        res = obj.is_valid()
        if res:
            models.Family.objects.filter(id=nid).update(**obj.cleaned_data)
            return redirect(reverse("app-base:familyList", args=(1, 1, )))
        else:
            return render(request, "baseinfo/familyModify.html", {"form": obj, "nid": nid})


@auth
def familyDetail(request, userID, nid):
    rec = models.Family.objects.filter(id=nid).first()
    dic = {
        "name": rec.name,
        "location": rec.location,
        "address": rec.address,
        "status": rec.status,
        "remark": rec.remark
    }
    obj = FormFamily(initial=dic)
    return render(request, "baseinfo/familyDetail.html", {"form": obj, "rec": rec})
