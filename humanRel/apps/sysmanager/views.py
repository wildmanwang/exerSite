from django.shortcuts import render, HttpResponse, redirect
from apps.sysmanager.models import User
from django.forms import Form, fields, widgets

# Create your views here.


class FormUser(Form):
    name = fields.CharField(
        label="用户名：",
        min_length=6,
        max_length=20,
        widget=widgets.TextInput(attrs={"class": "regType"}),
        error_messages={
            "min_length": "用户名长度不能小于6",
            "max_length": "用户名长度不能大于20"
        }
    )
    mobile = fields.CharField(
        label="手机号码：",
        min_length=11,
        max_length=11,
        widget=widgets.TextInput(attrs={"class": "regType"}),
        error_messages={
            "min_length": "手机号码长度不能小于11",
            "max_length": "手机号码长度不能大于11"
        }
    )
    email = fields.EmailField(
        label="电子邮箱：",
        required=False,
        widget=widgets.EmailInput(attrs={"class": "regType"})
    )
    loginPW = fields.CharField(
        label="登录密码：",
        widget=widgets.PasswordInput(attrs={"class": "regType"})
    )
    reloginPW = fields.CharField(
        label="确认登录密码：",
        widget=widgets.PasswordInput(attrs={"class": "regType"})
    )


def register(request):
    if request.method == "GET":
        obj = FormUser()
        return render(request, "sysmanager/register.html", {"form": obj})
    elif request.method == "POST":
        obj = FormUser(request.POST)
        loginPW = request.POST.get("password", None)
        reloginPW = request.POST.get("repassword", None)
        if loginPW != reloginPW:
            return render(request, "sysmanager/register.html", {"form": obj, "info": "两次输入的密码不同"})
        res = obj.is_valid()
        if res:
            obj.cleaned_data.pop("reloginPW")
            User.objects.create(**obj.cleaned_data)
            return redirect("sys/index")
        else:
            return render(request, "sysmanager/register.html", {"form": obj})


def login(request):
    if request.method == "GET":
        return render(request, "sysmanager/login.html", {"info": ""})
    elif request.method == "POST":
        username = request.POST.get("username", None)
        userpw = request.POST.get("userpw", None)
        if not username:
            return render(request, "sysmanager/login.html", {"info": "请输入用户名"})
        rec = User.objects.filter(name=username).first()
        if not rec:
            return render(request, "sysmanager/login.html", {"info": "用户名无效"})
        sPW = rec.loginPW
        if not sPW:
            sPW = ""
        if userpw != sPW:
            return render(request, "sysmanager/login.html", {"info": "密码错误"})
        request.session.set_expiry(36000)
        request.session["LoginUser"] = username
        return redirect("http://127.0.0.1:8000/sys/index")
    else:
        return HttpResponse("无效的请求方式：%s" % (request.method))


def auth(func):
    def inner(request, *args, **kwargs):
        user = request.session.get("LoginUser", None)
        if not user:
            return redirect("sys/login/")
        return func(request, *args, **kwargs)
    return inner


@auth
def index(request):
    if request.method == "GET":
        return render(request, "sysmanager/index.html")
