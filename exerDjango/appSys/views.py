from django.shortcuts import render, redirect

# Create your views here.

UserList = {
    {"ID": "aaa", "name": "张小慧", "gender": "女", "mobile": "13812346661", "position": "研发", "pwd": "111", "status": "正常"},
    {"ID": "bbb", "name": "李莉莉", "gender": "女", "mobile": "13812346662", "position": "研发", "pwd": "222", "status": "正常"},
    {"ID": "ccc", "name": "孙晓芸", "gender": "女", "mobile": "13812346663", "position": "研发", "pwd": "333", "status": "正常"},
    {"ID": "ddd", "name": "周芳芳", "gender": "女", "mobile": "13812346664", "position": "测试", "pwd": "444", "status": "正常"},
    {"ID": "eee", "name": "刘玉芳", "gender": "女", "mobile": "13812346665", "position": "测试", "pwd": "555", "status": "正常"},
    {"ID": "fff", "name": "王培培", "gender": "女", "mobile": "13812346666", "position": "测试", "pwd": "666", "status": "正常"}
}

def login(request):
    if request.method == "GET":
        return render(request, "login.html", {"info": ""})
    elif request.method == "POST":
        user = request.POST.get("user", None)
        pwd = request.POST.get("pwd", None)
        if user is None:
            return render(request, "login.html", {"info": "请输入用户ID！"})
        if user in UserList:
            if UserList[user]["pwd"] == pwd:
                return redirect("/employees")
            return render(request, "login.html", {"info": "密码错误！"})
        else:
            return render(request, "login.html", {"info": "查无此用户！"})

def employees(request):
    return render(request, "employees.html", UserList)

def employeesDetail(request):
    return render(request, "employees.html")

def employeesUpdate(request):
    return render(request, "employees.html")

def employeesDelete(request):
    return render(request, "employees.html")
