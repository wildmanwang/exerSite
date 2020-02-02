from django.shortcuts import render, HttpResponse, redirect
from sysmanager import models
from utils.pages import Pages
import json

# Create your views here.

def login(request):
    if request.method == "GET":
        rep = render(request, "login.html")
        rep.delete_cookie("curUser")
        return rep
    elif request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", "")
        if not password:
            password = ""
        data = models.Users.objects.filter(name=username).first()
        if not data:
            return render(request, "login.html", {"info": "查无此用户"})
        else:
            sPW = data.password
            if not sPW:
                sPW = ""
            if sPW != password:
                return render(request, "login.html", {"info": "密码错误"})
            rep = redirect("http://127.0.0.1:8000/myDesk")
            rep.set_cookie("curUser", username, max_age=3600)
            return rep

def auth(func):
    def inner(request, *args, **kwargs):
        cookieValue = request.COOKIES.get("curUser")
        if not cookieValue:
            return redirect("login/")
        return func(request, *args, **kwargs)
    return inner

@auth
def myDesk(request):
    return render(request, "myDesk.html", {"title": "", "type": 0})

@auth
def products(request, pageNo=1):
    data = models.Products.objects.all()
    cnt = request.COOKIES.get("reccnt_perpage")
    if not cnt:
        cnt = "10"
    page = Pages(len(data), int(cnt), "products-", pageNo)
    rep = render(request, "products.html", {"title": "商品", "type": 1, "ds": data[page.startRec:page.endRec], "pagetag": page.pageStr})
    rep.set_cookie("reccnt_perpage", cnt)
    return rep

@auth
def products_new(request):
    if request.method == "GET":
        return render(request, "products_new.html", {"title": "商品-新增", "type": 1})
    else:
        rtn = {
            "result": False,
            "info": None,
            "data": None
        }
        if request.method == "POST":
            if not rtn["info"]:
                col_code = request.POST.get("col_code", None)
                if not col_code:
                    rtn["info"] = "请输入商品编码"
            if not rtn["info"]:
                col_name = request.POST.get("col_name", None)
                if not col_name:
                    rtn["info"] = "请输入商品名称"
            if not rtn["info"]:
                col_price = request.POST.get("col_price", None)
                if not col_price:
                    rtn["info"] = "请输入商品参考价格"
            if not rtn["info"]:
                col_verMain = request.POST.get("col_verMain", None)
                if not col_verMain:
                    rtn["info"] = "请输入主版本号"
            if not rtn["info"]:
                col_verSub = request.POST.get("col_verSub", None)
                if not col_verSub:
                    rtn["info"] = "请输入子版本号"
            if not rtn["info"]:
                col_datePro = request.POST.get("col_datePro", None)
                if not col_datePro:
                    rtn["info"] = "请输入商品注册日期"
            if not rtn["info"]:
                col_dateCur = request.POST.get("col_dateCur", None)
                if not col_dateCur:
                    rtn["info"] = "请输入当前版本发布日期"
            if not rtn["info"]:
                col_remark = request.POST.get("col_remark", None)
            if not rtn["info"]:
                obj = models.Products.objects.create(
                    code=col_code,
                    name=col_name,
                    price=col_price,
                    verMain=col_verMain,
                    verSub=col_verSub,
                    datePro=col_datePro,
                    dateCur=col_dateCur,
                    remark=col_remark
                )
                if obj:
                    rtn["result"] = True
                else:
                    rtn["info"] = "数据保存失败"
        else:
            rtn["info"] = "没有定义的请求方法：{method}".format(method=request.method)
        return HttpResponse(json.dumps(rtn))

@auth
def products_modify(request, recid):
    if request.method == "GET":
        rec = models.Products.objects.filter(id=recid).first()
        return render(request, "products_modify.html", {"title": "商品-修改", "type": 1, "rec": rec})
    else:
        rtn = {
            "result": False,
            "info": None,
            "data": None
        }
        if request.method == "POST":
            if not rtn["info"]:
                col_code = request.POST.get("col_code", None)
                if not col_code:
                    rtn["info"] = "请输入商品编码"
            if not rtn["info"]:
                col_name = request.POST.get("col_name", None)
                if not col_name:
                    rtn["info"] = "请输入商品名称"
            if not rtn["info"]:
                col_price = request.POST.get("col_price", None)
                if not col_price:
                    rtn["info"] = "请输入商品参考价格"
            if not rtn["info"]:
                col_verMain = request.POST.get("col_verMain", None)
                if not col_verMain:
                    rtn["info"] = "请输入主版本号"
            if not rtn["info"]:
                col_verSub = request.POST.get("col_verSub", None)
                if not col_verSub:
                    rtn["info"] = "请输入子版本号"
            if not rtn["info"]:
                col_datePro = request.POST.get("col_datePro", None)
                if not col_datePro:
                    rtn["info"] = "请输入商品注册日期"
            if not rtn["info"]:
                col_dateCur = request.POST.get("col_dateCur", None)
                if not col_dateCur:
                    rtn["info"] = "请输入当前版本发布日期"
            if not rtn["info"]:
                col_status = request.POST.get("col_status", None)
                col_status = int(col_status)
            if not rtn["info"]:
                col_remark = request.POST.get("col_remark", None)
            if not rtn["info"]:
                try:
                    obj = models.Products.objects.filter(id=recid).update(
                        code=col_code,
                        name=col_name,
                        price=col_price,
                        verMain=col_verMain,
                        verSub=col_verSub,
                        datePro=col_datePro,
                        dateCur=col_dateCur,
                        status=col_status,
                        remark=col_remark
                    )
                    rtn["result"] = True
                except Exception as e:
                    rtn["info"] = str(e)
        else:
            rtn["info"] = "没有定义的请求方法：{method}".format(method=request.method)
        return HttpResponse(json.dumps(rtn))

@auth
def products_detail(request, recid):
    rec = models.Products.objects.filter(id=recid).first()
    return render(request, "products_detail.html", {"title": "商品-详情", "type": 1, "rec": rec})

@auth
def products_delete(request, recid):
    rtn = {
        "result": False,
        "info": None,
        "data": None
    }
    data = models.Products.objects.filter(id=recid)
    if not data:
        rtn["info"] = "查无此记录：[{recid}]".format(recid=recid)
    else:
        data.delete()
        rtn["result"] = True
    return HttpResponse(json.dumps(rtn))

@auth
def customers(request, pageNo=1):
    data = models.Customer.objects.all()
    cnt = request.COOKIES.get("reccnt_perpage")
    if not cnt:
        cnt = "10"
    page = Pages(len(data), int(cnt), "customers-", pageNo)
    rep = render(request, "customers.html", {"title": "客户", "type": 1, "ds": data[page.startRec:page.endRec], "pagetag": page.pageStr})
    rep.set_cookie("reccnt_perpage", cnt)
    return rep

@auth
def customers_new(request):
    if request.method == "GET":
        cusEmps = models.CusEmployee.objects.all()
        pros = models.Products.objects.all()
        return render(request, "customers_new.html", {"title": "客户-新增", "type": 1, "cusEmps": cusEmps, "pros": pros})
    else:
        rtn = {
            "result": False,
            "info": None,
            "data": None
        }
        if request.method == "POST":
            if not rtn["info"]:
                col_code = request.POST.get("col_code", None)
                if not col_code:
                    rtn["info"] = "请输入客户编码"
            if not rtn["info"]:
                col_name = request.POST.get("col_name", None)
                if not col_name:
                    rtn["info"] = "请输入客户名称"
            if not rtn["info"]:
                col_simpleName = request.POST.get("col_simpleName", None)
                if not col_simpleName:
                    rtn["info"] = "请输入简称"
            if not rtn["info"]:
                col_contactPerson = request.POST.get("col_contactPerson", None)
                col_contactPerson = int(col_contactPerson)
            if not rtn["info"]:
                col_address = request.POST.get("col_address", None)
            if not rtn["info"]:
                col_remark = request.POST.get("col_remark", None)
            if not rtn["info"]:
                obj = models.Customer.objects.create(
                    code=col_code,
                    name=col_name,
                    simpleName=col_simpleName,
                    contactPerson_id=col_contactPerson,
                    address=col_address,
                    remark=col_remark
                )
                if obj:
                    proItem = []
                    for item in request.POST.getlist("proItem", None):
                        proItem.append(int(item))
                    rel = models.Customer.objects.get(id=obj.id)
                    rel.products.set(proItem)
                    rtn["result"] = True
                else:
                    rtn["info"] = "数据保存失败"
        else:
            rtn["info"] = "没有定义的请求方法：{method}".format(method=request.method)
        return HttpResponse(json.dumps(rtn))

@auth
def customers_modify(request, recid):
    if request.method == "GET":
        rec = models.Customer.objects.filter(id=recid).first()
        cusEmps = models.CusEmployee.objects.all()
        pros = models.Products.objects.all()
        return render(request, "customers_modify.html", {"title": "客户-修改", "type": 1, "rec": rec, "cusEmps": cusEmps, "pros": pros})
    else:
        rtn = {
            "result": False,
            "info": None,
            "data": None
        }
        if request.method == "POST":
            if not rtn["info"]:
                col_code = request.POST.get("col_code", None)
                if not col_code:
                    rtn["info"] = "请输入客户编码"
            if not rtn["info"]:
                col_name = request.POST.get("col_name", None)
                if not col_name:
                    rtn["info"] = "请输入客户名称"
            if not rtn["info"]:
                col_simpleName = request.POST.get("col_simpleName", None)
                if not col_simpleName:
                    rtn["info"] = "请输入客户简称"
            if not rtn["info"]:
                col_contactPerson = request.POST.get("col_contactPerson", None)
            if not rtn["info"]:
                col_address = request.POST.get("col_address", None)
            if not rtn["info"]:
                col_status = request.POST.get("col_status", None)
                col_status = int(col_status)
            if not rtn["info"]:
                col_remark = request.POST.get("col_remark", None)
            if not rtn["info"]:
                try:
                    obj = models.Customer.objects.filter(id=recid).update(
                        code=col_code,
                        name=col_name,
                        simpleName=col_simpleName,
                        contactPerson_id=col_contactPerson,
                        address=col_address,
                        status=col_status,
                        remark=col_remark
                    )
                    if obj:
                        proItem = []
                        for item in request.POST.getlist("proItem", None):
                            proItem.append(int(item))
                        rel = models.Customer.objects.get(id=recid)
                        rel.products.set(proItem)
                        rtn["result"] = True
                    else:
                        rtn["info"] = "数据保存失败"
                except Exception as e:
                    rtn["info"] = str(e)
        else:
            rtn["info"] = "没有定义的请求方法：{method}".format(method=request.method)
        return HttpResponse(json.dumps(rtn))

@auth
def customers_detail(request, recid):
    rec = models.Customer.objects.filter(id=recid).first()
    return render(request, "customers_detail.html", {"title": "客户-详情", "type": 1, "rec": rec})

@auth
def customers_delete(request, recid):
    rtn = {
        "result": False,
        "info": None,
        "data": None
    }
    data = models.Customer.objects.filter(id=recid)
    if not data:
        rtn["info"] = "查无此记录：[{recid}]".format(recid=recid)
    else:
        data.delete()
        rtn["result"] = True
    return HttpResponse(json.dumps(rtn))

@auth
def cusEmployees(request, pageNo=1):
    data = models.CusEmployee.objects.all()
    cnt = request.COOKIES.get("reccnt_perpage")
    if not cnt:
        cnt = "10"
    page = Pages(len(data), int(cnt), "cusEmployees-", pageNo)
    rep = render(request, "cusEmployees.html", {"title": "联系人", "type": 1, "ds": data[page.startRec:page.endRec], "pagetag": page.pageStr})
    rep.set_cookie("reccnt_perpage", cnt)
    return rep

@auth
def cusEmployees_new(request):
    if request.method == "GET":
        return render(request, "cusEmployees_new.html", {"title": "联系人-新增", "type": 1})
    else:
        rtn = {
            "result": False,
            "info": None,
            "data": None
        }
        if request.method == "POST":
            if not rtn["info"]:
                col_name = request.POST.get("col_name", None)
                if not col_name:
                    rtn["info"] = "请输入联系人姓名"
            if not rtn["info"]:
                col_position = request.POST.get("col_position", None)
            if not rtn["info"]:
                col_mobile = request.POST.get("col_mobile", None)
            if not rtn["info"]:
                col_email = request.POST.get("col_email", None)
            if not rtn["info"]:
                col_remark = request.POST.get("col_remark", None)
            if not rtn["info"]:
                obj = models.CusEmployee.objects.create(
                    name=col_name,
                    position=col_position,
                    mobile=col_mobile,
                    email=col_email,
                    remark=col_remark
                )
                if obj:
                    rtn["result"] = True
                else:
                    rtn["info"] = "数据保存失败"
        else:
            rtn["info"] = "没有定义的请求方法：{method}".format(method=request.method)
        return HttpResponse(json.dumps(rtn))

@auth
def cusEmployees_modify(request, recid):
    if request.method == "GET":
        rec = models.CusEmployee.objects.filter(id=recid).first()
        return render(request, "cusEmployees_modify.html", {"title": "联系人-修改", "type": 1, "rec": rec})
    else:
        rtn = {
            "result": False,
            "info": None,
            "data": None
        }
        if request.method == "POST":
            if not rtn["info"]:
                col_name = request.POST.get("col_name", None)
                if not col_name:
                    rtn["info"] = "请输入联系人姓名"
            if not rtn["info"]:
                col_position = request.POST.get("col_position", None)
            if not rtn["info"]:
                col_mobile = request.POST.get("col_mobile", None)
            if not rtn["info"]:
                col_email = request.POST.get("col_email", None)
            if not rtn["info"]:
                col_status = request.POST.get("col_status", None)
                col_status = int(col_status)
            if not rtn["info"]:
                col_remark = request.POST.get("col_remark", None)
            if not rtn["info"]:
                try:
                    obj = models.CusEmployee.objects.filter(id=recid).update(
                        name=col_name,
                        position=col_position,
                        mobile=col_mobile,
                        email=col_email,
                        status=col_status,
                        remark=col_remark
                    )
                    rtn["result"] = True
                except Exception as e:
                    rtn["info"] = str(e)
        else:
            rtn["info"] = "没有定义的请求方法：{method}".format(method=request.method)
        return HttpResponse(json.dumps(rtn))

@auth
def cusEmployees_detail(request, recid):
    rec = models.CusEmployee.objects.filter(id=recid).first()
    return render(request, "cusEmployees_detail.html", {"title": "联系人-详情", "type": 1, "rec": rec})

@auth
def cusEmployees_delete(request, recid):
    rtn = {
        "result": False,
        "info": None,
        "data": None
    }
    data = models.CusEmployee.objects.filter(id=recid)
    if not data:
        rtn["info"] = "查无此记录：[{recid}]".format(recid=recid)
    else:
        data.delete()
        rtn["result"] = True
    return HttpResponse(json.dumps(rtn))