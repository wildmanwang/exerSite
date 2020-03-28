from django.shortcuts import HttpResponse, render, redirect
from appSys import models
import os, json


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


def index(request):
    return render(request, "sysfuncs/index.html")


def employees(request):
    return render(request, "functions/employees.html", {"users": models.Employee.objects.all()})


def employeesAllInOne(request):
    return render(request, "functions/employeesAllInOne.html", {"users": models.Employee.objects.all(), "dept": models.Department.objects.all(), "projects": models.Project.objects.all()})


def employeeDetail(request, userID):
    res = models.Employee.objects.filter(id=userID).first()
    if not res:
        return HttpResponse("<head><meta http-equiv='Refresh' Content='3;/employees'></head><body><h3>查无此员工!</h3></body>")
    else:
        return render(request, "functions/emp_detail.html", {"user": res})


def employeeNew(request):
    if request.method == "GET":
        return render(request, "functions/emp_new.html")
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


def employeeNewmany(request):
    rtn = {
        "result": True,
        "info": ""
    }
    if request.method == "POST":
        obj = models.Employee.objects.create(
            jobNumber=request.POST.get("jobNumber", None),
            name=request.POST.get("name", None),
            gender=request.POST.get("gender", None)
        )
        for pro in request.POST.getlist("projects", None):
            obj.rPro.add(pro)

    return HttpResponse(json.dumps(rtn))


def employeeUpdate(request, userID):
    if request.method == "GET":
        res = models.Employee.objects.filter(id=userID).first()
        if not res:
            return HttpResponse("<head><meta http-equiv='Refresh' Content='3;/employees'></head><body><h3>查无此员工!</h3></body>")
        dept = models.Department.objects.all()
        return render(request, "functions/emp_update.html", {"user": res, "dept": dept})
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


def employeeUpdatemany(request, userID):
    if request.method == "POST":
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
                    gender=request.POST.get("gender")
                )
                obj = models.Employee.objects.get(id=userID)
                obj.rPro.set(request.POST.getlist("projects"))
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
        res = models.Employee.objects.filter(id=userID).first()
        if not res:
            rtn["info"] = "userID:" + userID + "查无此员工！"
        else:
            models.Employee.objects.filter(id=userID).delete()
            rtn["result"] = True
    except Exception as e:
        rtn["info"] = str(e)

    return HttpResponse(json.dumps(rtn))


def employeeDeletemany(request):
    rtn = {
        "result": False,
        "info": None,
        "data": None
    }
    try:
        userID = request.POST.get("userID", None)
        res = models.Employee.objects.filter(id=userID).first()
        if not res:
            rtn["info"] = "userID:" + userID + "查无此员工！"
        else:
            res.rPro.clear()
            rtn["result"] = True
    except Exception as e:
        rtn["info"] = str(e)

    return HttpResponse(json.dumps(rtn))


PageDatas = []
for i in range(116):
    PageDatas.append(i)


def multipages(request, pageNo):
    from utils.pages import Pages

    page = Pages(len(PageDatas), 12, "/multipages-", pageNo)
    return render(request, "components/multipages.html", {"data": PageDatas[page.startRec:page.endRec], "pagetag": page.pageStr})


def uploadfile(request):
    if request.method == "GET":
        return render(request, "components/uploadfile.html")
    elif request.method == "POST":
        rtn = {
            "result": False,
            "data": None,
            "info": None
        }
        myfile = request.FILES.get("myfile")
        filename = os.path.join("static/upload", myfile.name)
        with open(filename, "wb") as f:
            for item in myfile.chunks():
                f.write(item)
        rtn["result"] = True
        rtn["data"] = filename
        rep =  HttpResponse(json.dumps(rtn))
        rep["X-Frame-Options"] = "SAMEORIGIN"               # 允许在Frame框架中显示

        return rep


def mykindeditor(request):
    return render(request, "components/mykindeditor.html")
