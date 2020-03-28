from django.shortcuts import render, redirect, reverse, HttpResponse
from apps.sysmanager.views import auth
from apps.blogs.models import Blog, BlogUpRecord
from datetime import datetime
from utils.pages import Pages
import json

# Create your views here.


@auth
def index(request, user, pageNo=1):
    dataList = Blog.objects.all().order_by("-id")
    cnt = request.COOKIES.get("reccnt_perpage")
    if not cnt:
        cnt = "10"
    page = Pages(len(dataList), int(cnt), "index-", pageNo)
    rep = render(request, "blogs/index.html", {"dataList": dataList[page.startRec:page.endRec], "pagetag": page.pageStr, "user": user})
    rep.set_cookie("reccnt_perpage", cnt, path="/")
    return rep


@auth
def blogNew(request, user):
    if request.method == "GET":
        return render(request, "blogs/blogNew.html", {"user": user})
    elif request.method == "POST":
        title = request.POST.get("blogTitle", None)
        contents = request.POST.get("blogContent", None)
        obj = Blog.objects.create(
            title=title,
            contents=contents,
            createTime=datetime.now(),
            upTimes=0,
            owner_id=user.id
        )
        return redirect(reverse("app-blogs:index", args=(1, )))


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