from django.shortcuts import render, redirect, reverse, HttpResponse
from apps.sysmanager.views import auth
from apps.blogs.models import Category, Article_type, Blog, BlogUpRecord
from django.db import transaction       # 事务管理
from datetime import datetime
from utils.pages import Pages
from utils.xss import XSSFilter
import json

# Create your views here.


@auth
def index(request, user, *args, **kwargs):
    condition = {}
    pageNo = 1
    for k, v in kwargs.items():
        kwargs[k] = int(v)
        if k == "pageNo":
            pageNo = v
        elif v == "0":
            pass
        else:
            condition[k] = v
    dataList = Blog.objects.filter(**condition).order_by("-id")
    cnt = request.COOKIES.get("reccnt_perpage")
    if not cnt:
        cnt = "10"
    page = Pages(len(dataList), int(cnt), "index-1-1-", pageNo)
    dsCategory = Category.objects.all()
    dsArticle_type = Article_type.objects.all()
    rep = render(
        request,
        "blogs/index.html", {
            "dataList": dataList[page.startRec:page.endRec],
            "pagetag": page.pageStr,
            "user": user,
            "dsCategory": dsCategory,
            "dsArticle_type": dsArticle_type,
            "kwargs": kwargs
        })
    rep.set_cookie("reccnt_perpage", cnt, path="/")
    return rep


@auth
def blogNew(request, user):
    if request.method == "GET":
        return render(request, "blogs/blogNew.html", {"user": user})
    elif request.method == "POST":
        title = request.POST.get("blogTitle", None)
        contents = request.POST.get("blogContent", None)
        contents = XSSFilter().process(contents)
        with transaction.Atomic(using=None, savepoint=True):
            # 全部数据库作为一个事务提交
            obj = Blog.objects.create(
                title=title,
                contents=contents,
                createTime=datetime.now(),
                upTimes=0,
                owner_id=user.id
            )
        return redirect(reverse("app-blogs:index", args=(1, 1, 1, )))


@auth
def blog(request, user, nid):
    if request.method == "GET":
        rec = Blog.objects.filter(id=nid).first()
        uprec = BlogUpRecord.objects.filter(blog=rec, upUser=user).first()
        if uprec:
            zan = 1
        else:
            zan = 0
        return render(request, "blogs/blog.html", {"rec": rec, "user": user, "zan": zan})


@auth
def blogZan(request, user):
    if request.method == "POST":
        rtn = {
            "result": False,
            "data": None,
            "info": None
        }
        blogID = request.POST.get("blogID", None)
        if blogID:
            blog=Blog.objects.filter(id=blogID).first()
            record = BlogUpRecord.objects.filter(blog__id=blogID, upUser=user).first()
            if record:
                num = blog.upTimes - 1
                Blog.objects.filter(id=blogID).update(upTimes=num)
                BlogUpRecord.objects.filter(blog__id=blogID, upUser=user).delete()
            else:
                num = blog.upTimes + 1
                Blog.objects.filter(id=blogID).update(upTimes=num)
                BlogUpRecord.objects.create(blog=blog, upUser=user)
            rtn["result"] = True
            rtn["data"] = num
        return HttpResponse(json.dumps(rtn))