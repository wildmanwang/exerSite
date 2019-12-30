from django.shortcuts import render, redirect, HttpResponse

# Create your views here.

UserList = [
    {"ID": "aaa", "name": "张小慧", "gender": "女", "mobile": "13812346661", "position": "研发", "pwd": "111", "status": "正常"},
    {"ID": "bbb", "name": "李莉莉", "gender": "女", "mobile": "13812346662", "position": "研发", "pwd": "222", "status": "正常"},
    {"ID": "ccc", "name": "孙晓芸", "gender": "女", "mobile": "13812346663", "position": "研发", "pwd": "333", "status": "正常"},
    {"ID": "ddd", "name": "周芳芳", "gender": "女", "mobile": "13812346664", "position": "测试", "pwd": "444", "status": "正常"},
    {"ID": "eee", "name": "刘玉芳", "gender": "女", "mobile": "13812346665", "position": "测试", "pwd": "555", "status": "正常"},
    {"ID": "fff", "name": "王培培", "gender": "女", "mobile": "13812346666", "position": "测试", "pwd": "666", "status": "正常"}
]

def login(request):
    if request.method == "GET":
        return render(request, "login.html", {"info": ""})
    elif request.method == "POST":
        user = request.POST.get("userID", None)
        pwd = request.POST.get("userPwd", None)
        if user is None:
            return render(request, "login.html", {"info": "请输入用户ID！"})
        for rec in UserList:
            if rec["ID"] == user and rec["pwd"] == pwd:
                return redirect("/employees")
        return render(request, "login.html", {"info": "用户或密码错误！"})

def employees(request):
    return render(request, "employees.html", {"users": UserList})

def employeeDetail(request):
    user = request.GET.get("userID", None)
    for rec in UserList:
        if rec["ID"] == user:
            return render(request, "emp_detail.html", {"user": rec})
    return HttpResponse("<head><meta http-equiv='Refresh' Content='3;/employees'><title>查无此员工</title></head><body><h3>查无此员工!</h3></body>")

def employeeNew(request):
    if request.method == "GET":
        return render(request, "emp_new.html")
    elif request.method == "POST":
        UserList.append({
            "ID": request.POST.get("ID", None),
            "name": request.POST.get("name", None),
            "gender": request.POST.get("gender", None),
            "mobile": request.POST.get("mobile", None),
            "position": request.POST.get("position", None),
            "pwd": request.POST.get("pwd", None),
            "status": request.POST.get("status", None)
        })
        return redirect("/employees")

def employeeUpdate(request):
    if request.method == "GET":
        user = request.GET.get("userID", None)
        for rec in UserList:
            if rec["ID"] == user:
                return render(request, "emp_update.html", {"user": rec})
        return HttpResponse("<head><meta http-equiv='Refresh' Content='3;/employees'><title>查无此员工</title></head><body><h3>查无此员工!</h3></body>")
    elif request.method == "POST":
        user = request.POST.get("ID", None)
        for rec in UserList:
            if rec["ID"] == user:
                rec["name"] = request.POST.get("name", None)
                if request.POST.get("gender", None) == "0":
                    rec["gender"] = "女"
                else:
                    rec["gender"] = "男"
                rec["mobile"] = request.POST.get("mobile", None)
                tmp = request.POST.get("position", None)
                if tmp == "1":
                    rec["position"] = "产品"
                elif tmp == "2":
                    rec["position"] = "研发"
                else:
                    rec["position"] = "测试"
                rec["pwd"] = request.POST.get("pwd", None)
                rec["status"] = request.POST.get("status", None)
                return redirect("/employees")
        return HttpResponse("<head><meta http-equiv='Refresh' Content='3;/employees'><title>查无此员工</title></head><body><h3>查无此员工!</h3></body>")

def employeeDelete(request):
    user = request.POST.get("userID", None)
    for rec in UserList:
        if rec["ID"] == user:
            UserList.remove(rec)
            return redirect("/employees")
    return HttpResponse("<head><meta http-equiv='Refresh' Content='3;/employees'><title>查无此员工</title></head><body><h3>查无此员工!</h3></body>")

