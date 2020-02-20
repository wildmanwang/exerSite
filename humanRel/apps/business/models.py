from django.db import models

# Create your models here.


class RelEvent(models.Model):
    user = models.ForeignKey(verbose_name="用户", to="sysmanager.User", related_name="relEventUser", null=True, on_delete=models.PROTECT)
    eventDate = models.DateField(verbose_name="事件日期")
    eventName = models.CharField(verbose_name="事件简称", max_length=50)
    family = models.ForeignKey(verbose_name="家庭", to="baseinfo.Family", related_name="eventFamily", on_delete=models.PROTECT)
    person = models.ForeignKey(verbose_name="当事人", to="baseinfo.Person", related_name="eventPerson", on_delete=models.PROTECT)
    eventType = models.IntegerField(verbose_name="事件类型", choices=((1, "结婚"), (2, "生子"), (3, "周岁"), (4, "祝寿"), (5, "考学"), (6, "乔迁"), (7, "身故"), (99, "其他")))
    formType = models.IntegerField(verbose_name="宴请类型", choices=((1, "隆重宴请"), (2, "亲朋小聚"), (3, "低调跳过"), (99, "待定")))
    eventDes = models.CharField(verbose_name="事件说明", max_length=255, null=True)
    direction = models.IntegerField(verbose_name="事件发起方", choices=((1, "我发起"), (2, "他人发起")))
    dateFrom = models.DateField(verbose_name="开始日期")
    dateTo = models.DateField(verbose_name="截止日期")
    amtOutFood = models.DecimalField(verbose_name="宴席支出金额", default=0.00, max_digits=10, decimal_places=2)
    amtOutOther = models.DecimalField(verbose_name="其他支出金额", default=0.00, max_digits=10, decimal_places=2)
    cntFamily = models.IntegerField(verbose_name="来宾户数", default=0)
    cntTable = models.IntegerField(verbose_name="宴席桌数", null=True)
    amtInBook = models.DecimalField(verbose_name="礼簿金额", default=0.00, max_digits=10, decimal_places=2)
    amtInOther = models.DecimalField(verbose_name="其他收入金额", default=0.00, max_digits=10, decimal_places=2)
    status = models.IntegerField(verbose_name="状态", choices=((1, "预测"), (2, "计划"), (9, "完成")))
    remark = models.CharField(verbose_name="备注", max_length=255, null=True)

    def __str__(self):
        return self.eventName


class JoinRecord(models.Model):
    user = models.ForeignKey(verbose_name="用户", to="sysmanager.User", related_name="joinRecordUser", null=True, on_delete=models.PROTECT)
    event = models.ForeignKey(verbose_name="事件", to="RelEvent", related_name="recordEvent", on_delete=models.PROTECT)
    joinFamily = models.ForeignKey(verbose_name="出席家庭", to="baseinfo.Family", related_name="familyJoin", on_delete=models.PROTECT)
    amtBook = models.DecimalField(verbose_name="礼金", default=0.00, max_digits=10, decimal_places=2)
    amtOther = models.DecimalField(verbose_name="其他支出", default=0.00, max_digits=10, decimal_places=2)
    recTime = models.DateTimeField(verbose_name="登记时间", null=True)
    remark = models.CharField(verbose_name="备注", max_length=255, null=True)

    def __str__(self):
        return self.joinFamily.name
