from django.db import models

# Create your models here.


class areaLever(models.Model):
    lever = models.IntegerField(verbose_name="级别", choices=((1, "省"), (2, "市"), (3, "县/区"), (4, "镇/街道")))
    name = models.CharField(verbose_name="名称", max_length=50)
    super = models.ForeignKey(verbose_name="上级", to="areaLever", null=True, on_delete=models.SET_NULL)
    remark = models.TextField(verbose_name="备注", null=True)

    def __str__(self):
        return self.name


class User(models.Model):
    code = models.CharField(verbose_name="用户名", max_length=50)
    nickname = models.CharField(verbose_name="昵称", max_length=50)
    mobile = models.CharField(verbose_name="手机号码", max_length=20)
    email = models.EmailField(verbose_name="电子邮箱", null=True)
    password = models.CharField(verbose_name="密码", max_length=50)
    userStatus = models.IntegerField(verbose_name="用户状态", choices=((0, "无效"), (1, "正常")), default=1)

    openBlog = models.IntegerField(verbose_name="博客状态", choices=((0, "未开放"), (1, "已开放"), (2, "临时封号"), (3, "主动停号"), (9, "永久封号")), default=0)
    blogAddress = models.CharField(verbose_name="博客域名", max_length=50, null=True)
    blogSkin = models.CharField(verbose_name="博客皮肤", max_length=50, default="default")
    name = models.CharField(verbose_name="姓名", max_length=50, null=True)
    gender = models.IntegerField(verbose_name="性别", choices=((0, "女"), (1, "男")), null=True)
    birthdate = models.DateField(verbose_name="出生日期", null=True)
    imgName = models.CharField(verbose_name="头像文件名称", max_length=255, null=True)
    homeProvince = models.ForeignKey(verbose_name="家乡省份", to="areaLever", related_name="homeProvince", null=True, on_delete=models.SET_NULL)
    homeCity = models.ForeignKey(verbose_name="家乡城市", to="areaLever", related_name="homeCity", null=True, on_delete=models.SET_NULL)
    liveProvince = models.ForeignKey(verbose_name="居住省份", to="areaLever", related_name="liveProvince", null=True, on_delete=models.SET_NULL)
    liveCity = models.ForeignKey(verbose_name="居住城市", to="areaLever", related_name="liveCity", null=True, on_delete=models.SET_NULL)
    marriage = models.IntegerField(verbose_name="婚姻状况", choices=((1, "单身"), (2, "热恋"), (3, "订婚"), (4, "已婚"), (9, "离异")), null=True)
    position = models.CharField(verbose_name="职位", max_length=50, null=True)
    company = models.CharField(verbose_name="单位", max_length=50, null=True)
    work = models.IntegerField(verbose_name="工作状况", choices=((1, "学生"), (2, "待业"), (3, "就业"), (9, "其他")), null=True)


    def __str__(self):
        return self.nickname
