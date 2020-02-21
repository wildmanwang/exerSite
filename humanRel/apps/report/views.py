from django.shortcuts import render
from django.db.models import Count, Sum
from apps.business.models import JoinRecord
from apps.baseinfo.models import Person
from utils.pages import Pages
from apps.sysmanager.views import auth
from datetime import datetime, date

# Create your views here.


@auth
def repRelSum(request, userID):
    dateFrom = request.GET.get("from", None)
    dateTo = request.GET.get("to", None)
    eventType = request.GET.get("eventType", "0")
    pageNo = request.GET.get("pageNo", "1")
    if not dateFrom or not dateTo:
        if not dateFrom:
            dateFrom = date.today()
        if not dateTo:
            dateTo = date.today()
        dataList = []
    else:
        dateFrom = datetime.strptime(dateFrom, "%Y-%m-%d")
        dateTo = datetime.strptime(dateTo, "%Y-%m-%d")
        if not eventType or eventType == "0":
            dataList = JoinRecord.objects.filter(user=userID, event__eventDate__gte=dateFrom, event__eventDate__lte=dateTo).values("event__family__name__name").annotate(timesRel=Count("event"), timesJoin=Count("id"), amtJoin=Sum("amtBook"), amtOther=Sum("amtOther"))
        else:
            dataList = JoinRecord.objects.filter(user=userID, event__eventDate__gte=dateFrom, event__eventDate__lte=dateTo, event__eventType=int(eventType)).values("event__family__name__name").annotate(timesRel=Count("event"), timesJoin=Count("id"), amtJoin=Sum("amtBook"), amtOther=Sum("amtOther"))
    cnt = request.COOKIES.get("reccnt_perpage")
    if not cnt:
        cnt = "10"
    page = Pages(len(dataList), int(cnt), "repRelSum?eventType=%s&pageNo=%s" % (eventType, pageNo))
    rep = render(request, "report/repRelSum.html", {"dataList": dataList[page.startRec:page.endRec], "from": dateFrom, "to": dateTo, "eventType": eventType, "pageNo": pageNo, "pagetag": page.pageStr, "recCnt": len(dataList)})
    rep.set_cookie("reccnt_perpage", cnt, path="/rep/")
    return rep


@auth
def repRelDetail(request, userID):
    dateFrom = request.GET.get("from", None)
    dateTo = request.GET.get("to", None)
    eventType = request.GET.get("eventType", "0")
    pageNo = request.GET.get("pageNo", "1")
    if not dateFrom or not dateTo:
        if not dateFrom:
            dateFrom = date.today()
        if not dateTo:
            dateTo = date.today()
        dataList = []
    else:
        dateFrom = datetime.strptime(dateFrom, "%Y-%m-%d")
        dateTo = datetime.strptime(dateTo, "%Y-%m-%d")
        if not eventType or eventType == "0":
            dataList = JoinRecord.objects.filter(user=userID, event__eventDate__gte=dateFrom, event__eventDate__lte=dateTo)
        else:
            dataList = JoinRecord.objects.filter(user=userID, event__eventDate__gte=dateFrom, event__eventDate__lte=dateTo, event__eventType=int(eventType))
    cnt = request.COOKIES.get("reccnt_perpage")
    if not cnt:
        cnt = "10"
    page = Pages(len(dataList), int(cnt), "repRelDetail?eventType=%s&pageNo=%s" % (eventType, pageNo))
    rep = render(request, "report/repRelDetail.html", {"dataList": dataList[page.startRec:page.endRec], "from": dateFrom, "to": dateTo, "eventType": eventType, "pageNO": pageNo, "pagetag": page.pageStr, "recCnt": len(dataList)})
    rep.set_cookie("reccnt_perpage", cnt, path="/rep/")
    return rep


@auth
def repRelForecast(request, userID):
    dateFrom = request.GET.get("from", None)
    dateTo = request.GET.get("to", None)
    eventType = request.GET.get("eventType", "0")
    pageNo = request.GET.get("pageNo", "1")
    if not dateFrom or not dateTo:
        if not dateFrom:
            dateFrom = date.today()
        if not dateTo:
            dateTo = date.today()
        dataList = []
    else:
        dateFrom = datetime.strptime(dateFrom, "%Y-%m-%d")
        dateTo = datetime.strptime(dateTo, "%Y-%m-%d")
        if not eventType or eventType == "0":
            dataList = []
        else:
            dataList = []
    cnt = request.COOKIES.get("reccnt_perpage")
    if not cnt:
        cnt = "10"
    page = Pages(len(dataList), int(cnt), "repRelForecast?eventType=%s&pageNo=%s" % (eventType, pageNo))
    rep = render(request, "report/repRelForecast.html", {"dataList": dataList[page.startRec:page.endRec], "from": dateFrom, "to": dateTo, "eventType": eventType, "pageNO": pageNo, "pagetag": page.pageStr, "recCnt": len(dataList)})
    rep.set_cookie("reccnt_perpage", cnt, path="/rep/")
    return rep


@auth
def repRelMap(request, userID):
    person1 = request.GET.get("person1", None)
    person2 = request.GET.get("person2", None)
    dataList = []
    personList = Person.objects.all()
    rep = render(request, "report/repRelMap.html", {"dataList": dataList, "person1": person1, "person2": person2, "personList": personList, "recCnt": len(dataList)})
    return rep
