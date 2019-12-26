from django.shortcuts import render
from django.shortcuts import redirect

def login(request):
    info = ""
    if request.method == "GET":
        pass
    elif request.method == "POST":
        user = request.POST.get('user', None)
        password = request.POST.get('password', None)
        if user == "wlq" and password == "123":
            return redirect("/home")
        else:
            info = "用户名或密码错误！"

    return render(request, "login.html", {"msg_info":info})


user_list = [
    {"name": "张惠妹", "gender": "女", "email": "111@126.com"},
    {"name": "林心如", "gender": "女", "email": "112@126.com"},
    {"name": "赵敏", "gender": "女", "email": "113@126.com"},
    {"name": "黄蓉", "gender": "女", "email": "114@126.com"},
]


def home(request):
    if request.method == "POST":
        user_list.append({
            "name": request.POST.get("name", None),
            "gender": request.POST.get("gender", None),
            "email": request.POST.get("email", None)
        })
    return render(request, "home.html", {"user_list":user_list})

# Create your views here.
