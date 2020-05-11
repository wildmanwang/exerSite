from django.shortcuts import render, redirect, HttpResponse, reverse
from django.forms import ModelForm
from django.forms import widgets as wis     # 重命名防名称冲突
from apps.sysmanager.views import auth
from apps.backend.models import User, areaLever
from apps.sysmanager.views import MfUser
import os, json

# Create your views here.


class MfUserInfo(ModelForm):
    class Meta:
        model = User
        fields = ["name", "gender", "birthdate", "homeProvince", "homeCity", "liveProvince", "liveCity", "marriage", "position", "company", "work"]
        help_texts = {
            "name": "请输入姓名",
            "gender": "请选择性别",
            "birthdate": "请选择出生日期",
            "homeProvince": "请选择籍贯省份",
            "homeCity": "请选择籍贯城市",
            "liveProvince": "请选择居住省份",
            "liveCity": "请选择居住城市",
            "marriage": "请选择婚姻状况",
            "position": "请输入工作职位",
            "company": "请输入所在公司",
            "work": "请选择工作状况"
        }
        widgets = {
            "gender": wis.RadioSelect(choices=((0, "女"), (1, "男"))),
            "homeProvince": wis.Select(attrs={"class": "inputType"}),
            "homeCity": wis.Select(attrs={"class": "inputType"}, choices=areaLever.objects.filter(lever=2).values_list("id", "name")),
            "liveProvince": wis.Select(attrs={"class": "inputType"}, choices=areaLever.objects.filter(lever=1).values_list("id", "name")),
            "liveCity": wis.Select(attrs={"class": "inputType"}, choices=areaLever.objects.filter(lever=2).values_list("id", "name")),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 批量更新样式
        for col in iter(self.fields):
            if col != "gender":
                self.fields[col].widget.attrs.update({"class": "inputType"})
            self.fields[col].required = False


@auth
def setUser(request, user):
    if request.method == "GET":
        rec = User.objects.filter(id=user.id).first()
        mf = MfUser(instance=rec)
        return render(request, "backend/setUser.html", {"menuItem": "user", "rec": mf})
    elif request.method == "POST":
        rec = User.objects.filter(id=user.id).first()
        mf = MfUser(request.POST, instance=rec)
        if mf.is_valid():
            mf.save()
            return redirect(reverse("app-blogs:index", args=(1, 1, 1, )))
        else:
            return render(request, "backend/setUser.html", {"menuItem": "user", "rec": mf})


@auth
def setAcct(request, user):
    if request.method == "GET":
        rec = User.objects.filter(id=user.id).first()
        mf = MfUserInfo(instance=rec)
        return render(request, "backend/setAcct.html", {"menuItem": "acct", "rec": mf})
    elif request.method == "POST":
        rec = User.objects.filter(id=user.id).first()
        mf = MfUserInfo(request.POST, instance=rec)
        if mf.is_valid():
            mf.save()
            return redirect(reverse("app-blogs:index", args=(1, 1, 1, )))
        else:
            return render(request, "backend/setAcct.html", {"menuItem": "acct", "rec": mf})


@auth
def setPhoto(request, user):
    if request.method == "GET":
        return render(request, "backend/setPhoto.html", {"menuItem": "photo", "filename": User.objects.filter(id=user.id).first().imgName})
    elif request.method == "POST":
        rtn = {
            "result": False,
            "data": None,
            "info": None
        }
        myfile = request.FILES.get("myImg")
        filename = myfile.name
        filename = str(user.id) + filename[filename.find("."):]
        filename = os.path.join(r"static\upload", filename)
        with open(filename, "wb") as f:
            for item in myfile.chunks():
                f.write(item)
        rtn["result"] = True
        rtn["data"] = "\\" + filename
        rep = HttpResponse(json.dumps(rtn))
        rep["X-Frame-Options"] = "SAMEORIGIN"  # 允许在Frame框架中显示
        User.objects.filter(id=user.id).update(imgName=rtn["data"])

        return rep


@auth
def setBlog(request, user):
    return render(request, "backend/setBlog.html", {"menuItem": "blog"})


@auth
def myblogs(request, user):
    return render(request, "backend/myblogs.html")
