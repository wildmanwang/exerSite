from django.shortcuts import render, HttpResponse, redirect, reverse
from django.forms import ModelForm, fields, widgets
from apps.backend.models import User
import json
from django.core.exceptions import ValidationError

# Create your views here.


class MfUser(ModelForm):
    re_password = fields.CharField(
        label="确认密码",
        max_length=50,
        widget=widgets.PasswordInput(attrs={"class": "inputType"}),
        help_text="请确认用户密码"
    )
    class Meta:
        model = User
        fields = ["code", "nickname", "mobile", "email", "password"]
        help_texts = {"code": "请输入用户名", "nickname": "请输入用户昵称", "mobile": "请输入手机号码", "email": "请输入电子邮箱", "password": "请输入用户密码"}
        widgets = {
            "code": widgets.TextInput(attrs={"class": "inputType"}),
            "nickname": widgets.TextInput(attrs={"class": "inputType"}),
            "mobile": widgets.TextInput(attrs={"class": "inputType"}),
            "email": widgets.EmailInput(attrs={"class": "inputType"}),
            "password": widgets.PasswordInput(attrs={"class": "inputType"})
        }

    def clean(self):
        p1 = self.cleaned_data["password"]
        p2 = self.cleaned_data["re_password"]
        if p1 != p2:
            raise ValidationError("两次输入的密码不同")
        return self.cleaned_data


def register(request):
    if request.method == "GET":
        mf = MfUser()
        return render(request, "sysmanager/register.html", {"rec": mf})
    elif request.method == "POST":
        mf = MfUser(request.POST)
        if mf.is_valid():
            mf.save()
            return redirect("app-sys:login")
        else:
            return render(request, "sysmanager/register.html", {"rec": mf})


def login(request):
    if request.method == "GET":
        return render(request, "sysmanager/login.html")
    elif request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        rst = User.objects.filter(code=username).first()
        if not rst:
            return render(request, "sysmanager/login.html", {"info": "用户名无效"})
        if password != rst.password:
            return render(request, "sysmanager/login.html", {"info": "密码错误"})
        request.session.set_expiry(36000)
        request.session["LoginUser"] = username
        return redirect("app-blogs:index")


def logout(request):
    rtn = {
        "result": False,
        "data": None,
        "info": None
    }
    try:
        del request.session["LoginUser"]
        rtn["result"] = True
    except Exception as e:
        rtn["info"] = str(e)
    return HttpResponse(json.dumps(rtn))


def auth(func):
    def inner(request, *args, **kwargs):
        userName = request.session.get("LoginUser", None)
        if not userName:
            return redirect(reverse("app-sys:login"))
        user = User.objects.filter(code=userName).first()
        if not user:
            return redirect(reverse("app-sys:login"))
        return func(request, user, *args, **kwargs)
    return inner
