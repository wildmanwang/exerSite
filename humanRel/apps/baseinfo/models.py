from django.db import models

# Create your models here.


class Person(models.Model):
    user = models.ForeignKey(verbose_name="用户", to="sysmanager.User", related_name="personUser", null=True, on_delete=models.PROTECT)
    name = models.CharField(verbose_name="姓名", max_length=50)
    gender = models.IntegerField(verbose_name="性别", choices=((0, "女"), (1, "男")))
    birthDate = models.DateField(verbose_name="出生日期", null=True)
    relType = models.IntegerField(verbose_name="关系类型", choices=((0, "自己"), (1, "族亲"), (2, "姻亲"), (3, "同学"), (4, "朋友"), (5, "同事"), (6, "战友"), (7, "街坊"), (99, "其他")))
    family = models.ForeignKey(verbose_name="家庭", to="Family", related_name="personFamily", null=True, on_delete=models.SET_NULL)
    father = models.ForeignKey(verbose_name="父亲", to="Person", related_name="personFather", null=True, on_delete=models.SET_NULL)
    mother = models.ForeignKey(verbose_name="母亲", to="Person", related_name="personMother", null=True, on_delete=models.SET_NULL)
    Marriage = models.IntegerField(verbose_name="婚姻状况", choices=((0, "未婚"), (1, "已婚")), default=0)
    spouse = models.ForeignKey(verbose_name="配偶", to="Person", related_name="personSpuse", null=True, on_delete=models.SET_NULL)
    mobile = models.CharField(verbose_name="手机号码", max_length=20, null=True)
    weixin = models.CharField(verbose_name="微信号码", max_length=50, null=True)
    email = models.CharField(verbose_name="电子邮箱", max_length=255, null=True)
    address = models.CharField(verbose_name="现住址", max_length=255, null=True)
    workUnit = models.CharField(verbose_name="工作单位", max_length=50, null=True)
    education = models.IntegerField(verbose_name="学历", choices=((0, "在读"), (1, "小学"), (2, "初中"), (3, "高中"), (4, "大专"), (5, "本科"), (6, "硕士"), (7, "博士"), (99, "其他")))
    occupation = models.CharField(verbose_name="职业", max_length=20, null=True)
    status = models.IntegerField(verbose_name="状态", choices=((0, "失效"), (1, "正常")), default=1)
    remark = models.CharField(verbose_name="备注", max_length=255, null=True)

    def __str__(self):
        return self.name


class Family(models.Model):
    user = models.ForeignKey(verbose_name="用户", to="sysmanager.User", related_name="FamilyUser", null=True, on_delete=models.PROTECT)
    name = models.ForeignKey(verbose_name="家长", to="Person", related_name="FamilyName", on_delete=models.PROTECT)
    location = models.CharField(verbose_name="所在城市/村镇", max_length=50)
    address = models.CharField(verbose_name="家庭住址", max_length=255, null=True)
    status = models.IntegerField(verbose_name="状态", choices=((0, "失效"), (1, "正常")), default=1)
    remark = models.CharField(verbose_name="备注", max_length=255, null=True)

    def __str__(self):
        return self.name.name
