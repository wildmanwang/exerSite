from django.shortcuts import HttpResponse, render, redirect
from appSys import models
import json


# Create your views here.


def login(request):
    if request.method == "GET":
        return render(request, "login.html", {"info": ""})
    elif request.method == "POST":
        user = request.POST.get("userID", None)
        pwd = request.POST.get("userPwd", None)
        if not user:
            return render(request, "login.html", {"info": "请输入用户ID！"})
        res = models.Employee.objects.filter(jobNumber=user).first()
        if not res:
            return render(request, "login.html", {"info": "查无此操作员：[" + user + "]"})
        if res.pwd == pwd:
            return redirect("/employees")
        else:
            return render(request, "login.html", {"info": "用户或密码错误！"})


def employees(request):
    return render(request, "employees.html", {"users": models.Employee.objects.all()})


def employeesAllInOne(request):
    return render(request, "employeesAllInOne.html", {"users": models.Employee.objects.all(), "dept": models.Department.objects.all()})


def employeeDetail(request, userID):
    res = models.Employee.objects.filter(id=userID).first()
    if not res:
        return HttpResponse("<head><meta http-equiv='Refresh' Content='3;/employees'></head><body><h3>查无此员工!</h3></body>")
    else:
        return render(request, "emp_detail.html", {"user": res})


def employeeNew(request):
    if request.method == "GET":
        print(request.method)
        return render(request, "emp_new.html")
    elif request.method == "POST":
        rtn = {
            "result": False,
            "info": None,
            "data": None
        }
        try:
            userID = request.POST.get("jobNumber")
            res = models.Employee.objects.filter(jobNumber=userID)
            if not userID or len(userID) < 4:
                rtn["info"] = "工号无效！"
            elif res.count() > 0:
                rtn["info"] = "工号" + userID + "已存在！"
            else:
                models.Employee.objects.create(
                    jobNumber=request.POST.get("jobNumber"),
                    name=request.POST.get("name"),
                    gender=request.POST.get("gender"),
                    position=request.POST.get("position"),
                    email=request.POST.get("email"),
                    phone=request.POST.get("phone"),
                    dept_id=request.POST.get("dept_id"),
                    pwd=request.POST.get("pwd")
                )
                rtn["result"] = True
        except Exception as e:
            rtn["info"] = str(e)
        return HttpResponse(json.dumps(rtn))


def employeeUpdate(request, userID):
    if request.method == "GET":
        res = models.Employee.objects.filter(id=userID).first()
        if not res:
            return HttpResponse("<head><meta http-equiv='Refresh' Content='3;/employees'></head><body><h3>查无此员工!</h3></body>")
        dept = models.Department.objects.all()
        return render(request, "emp_update.html", {"user": res, "dept": dept})
    elif request.method == "POST":
        rtn = {
            "result": False,
            "info": None,
            "data": None
        }
        try:
            if not userID or len(userID) == 0:
                rtn["info"] = "员工ID无效"
            else:
                models.Employee.objects.filter(id=userID).update(
                    jobNumber=request.POST.get("jobNumber"),
                    name=request.POST.get("name"),
                    gender=request.POST.get("gender"),
                    position=request.POST.get("position"),
                    email=request.POST.get("email"),
                    phone=request.POST.get("phone"),
                    dept_id=request.POST.get("dept_id"),
                    pwd=request.POST.get("pwd")
                )
                rtn["result"] = True
        except Exception as e:
            rtn["info"] = str(e)

        return HttpResponse(json.dumps(rtn))


def employeeDelete(request):
    rtn = {
        "result": False,
        "info": None,
        "data": None
    }
    try:
        userID = request.POST.get("userID", None)
        print(userID)
        res = models.Employee.objects.filter(id=userID).first()
        if not res:
            print(request.POST)
            rtn["info"] = "userID:" + userID + "查无此员工！"
        else:
            models.Employee.objects.filter(id=userID).delete()
            rtn["result"] = True
    except Exception as e:
        rtn["info"] = str(e)

    return HttpResponse(json.dumps(rtn))
