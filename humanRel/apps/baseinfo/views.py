from django.shortcuts import render, HttpResponse, redirect
from apps.baseinfo import models
from django.forms import Form, fields, widgets
from django import forms
from utils.pages import Pages
import json

# Create your views here.


class FormPerson(Form):
    name = fields.CharField(
        label="姓名：",
        max_length=50,
        widget=widgets.TextInput(attrs={"class": "inputType"}),
        error_messages={"max_length": "姓名长度不能大于50"}
    )
    gender = fields.IntegerField(
        label="性别：",
        widget=widgets.RadioSelect(choices=((0, "女"), (1, "男")), attrs={"class": "inputOther"})
    )
    birthDate = fields.DateField(
        label="出生日期：",
        widget=widgets.DateInput(attrs={"class": "inputType"}),
        required=False
    )
    relType = fields.IntegerField(
        label="关系类型：",
        widget=widgets.Select(choices=((0, ""), (1, "血亲"), (2, "姻亲"), (3, "同学"), (4, "朋友"), (5, "同事"), (6, "战友"), (7, "街坊"), (8, "其他")), attrs={"class": "inputType"})
    )
    family = forms.ModelChoiceField(
        label="家庭：",
        widget=widgets.Select(attrs={"class": "inputType"}),
        queryset=models.Family.objects.all(),
        required=False
    )
    father = forms.ModelChoiceField(
        label="父亲：",
        widget=widgets.Select(attrs={"class": "inputType"}),
        queryset=models.Person.objects.filter(gender=1, Marriage=1),
        required=False
    )
    mother = forms.ModelChoiceField(
        label="母亲：",
        widget=widgets.Select(attrs={"class": "inputType"}),
        queryset=models.Person.objects.filter(gender=0, Marriage=1),
        required=False
    )
    Marriage = fields.IntegerField(
        label="婚姻状态：",
        widget=widgets.RadioSelect(choices=((0, "未婚"), (1, "已婚")), attrs={"class": "inputOther"})
    )
    spouse = forms.ModelChoiceField(
        label="配偶",
        widget=widgets.Select(attrs={"class": "inputType"}),
        queryset=models.Person.objects.all(),
        required=False
    )
    mobile = fields.CharField(
        label="手机号码：",
        min_length=11,
        max_length=11,
        widget=widgets.TextInput(attrs={"class": "inputType"}),
        required=False,
        error_messages={"min_length": "手机号码应该11位", "max_length": "手机号码应该11位"}
    )
    weixin = fields.CharField(
        label="微信号：",
        max_length=50,
        widget=widgets.TextInput(attrs={"class": "inputType"}),
        required=False,
        error_messages={"max_length": "微信号码不能大于50位"}
    )
    email = fields.EmailField(
        label="电子邮箱：",
        max_length=255,
        widget=widgets.EmailInput(attrs={"class": "inputType"}),
        required=False,
        error_messages={"max_length": "电子邮箱不能大于255位"}
    )
    address = fields.CharField(
        label="现住址：",
        max_length=255,
        widget=widgets.TextInput(attrs={"class": "inputType"}),
        required=False,
        error_messages={"max_length": "现住址不能大于255位"}
    )
    workUnit = fields.CharField(
        label="工作单位：",
        max_length=50,
        widget=widgets.TextInput(attrs={"class": "inputType"}),
        required=False,
        error_messages={"max_length": "工作单位不能大于50位"}
    )
    education = fields.IntegerField(
        label="学历：",
        widget=widgets.Select(choices=((-1, ""), (0, "在读"), (1, "小学"), (2, "初中"), (3, "高中"), (4, "大专"), (5, "本科"), (6, "硕士"), (7, "博士"), (0, "其他")), attrs={"class": "inputType"})
    )
    occupation = fields.CharField(
        label="职业：",
        max_length=20,
        widget=widgets.TextInput(attrs={"class": "inputType"}),
        required=False,
        error_messages={"max_length": "职业不能大于20位"}
    )
    status = fields.IntegerField(
        label="状态",
        initial=1,
        widget=widgets.RadioSelect(choices=((0, "失效"), (1, "正常")))
    )
    remark = fields.CharField(
        label="备注：",
        max_length=255,
        widget=widgets.TextInput(attrs={"class": "inputType"}),
        required=False,
        error_messages={"max_length": "备注不能大于255位"}
    )


def personList(request, status=9, pageNo=1):
    status = int(status)
    if status != 0 and status != 1:
        dataList = models.Person.objects.all()
    else:
        dataList = models.Person.objects.filter(status=status)
    cnt = request.COOKIES.get("reccnt_perpage")
    print(cnt)
    if not cnt:
        cnt = "10"
    page = Pages(len(dataList), int(cnt), "personList-%d-" % (status), pageNo)
    rep = render(request, "baseinfo/personList.html", {"dataList": dataList[page.startRec:page.endRec], "pagetag": page.pageStr, "status": status})
    rep.set_cookie("reccnt_perpage", cnt, path="/base/")
    return rep


def personNew(request):
    if request.method == "GET":
        obj = FormPerson()
        return render(request, "baseinfo/personNew.html", {"form": obj})
    elif request.method == "POST":
        obj = FormPerson(request.POST)
        res = obj.is_valid()
        if res:
            models.Person.objects.create(**obj.cleaned_data)
            return redirect("http://127.0.0.1:8000/base/personList-1-1")
        else:
            print(obj.errors)
            return render(request, "baseinfo/personNew.html", {"form": obj})


def personDelete(request, id):
    rtn = {
        "result": False,
        "data": None,
        "info": None
    }
    rec = models.Person.objects.filter(id=id).first()
    if not rec:
        rtn["info"] = "查无此记录%d" % (id)
    else:
        rec.delete()
        rtn["result"] = True
    return HttpResponse(json.dumps(rtn))


def personModify(request, id):
    if request.method == "GET":
        rec = models.Person.objects.filter(id=id).first()
        dic = {
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
        obj = FormPerson(initial=dic)
        return render(request, "baseinfo/personModify.html", {"form": obj, "id": id})
    elif request.method == "POST":
        obj = FormPerson(request.POST)
        res = obj.is_valid()
        if res:
            models.Person.objects.filter(id=id).update(**obj.cleaned_data)
            return redirect("http://127.0.0.1:8000/base/personList-1-1")
        else:
            return render(request, "baseinfo/personModify.html", {"form": obj, "id": id})


def personDetail(request, id):
    rec = models.Person.objects.filter(id=id).first()
    obj = FormPerson()
    return render(request, "baseinfo/personDetail.html", {"form": obj, "rec": rec})
