from django.db import models

# Create your models here.


class Parameters(models.Model):
    user = models.ForeignKey(verbose_name="用户", to="sysmanager.User", related_name="parametersUser", null=True, on_delete=models.PROTECT)
    code = models.CharField(verbose_name="代码", max_length=50)
    name = models.CharField(verbose_name="名称", max_length=50)
    pClass = models.IntegerField(verbose_name="分类", choices=((1, "系统"), (2, "资料"), (3, "往来"), (4, "报表"), (99, "其他")))
    sValue = models.CharField(verbose_name="参数值", max_length=255)
    remark = models.CharField(verbose_name="备注", max_length=255, null=True)


class User(models.Model):
    name = models.CharField(verbose_name="用户名", max_length=50)
    person = models.ForeignKey(verbose_name="人员", to="baseinfo.Person", related_name="userPerson", null=True, on_delete=models.SET_NULL)
    mobile = models.CharField(verbose_name="手机号码", max_length=20, null=True)
    email = models.CharField(verbose_name="电子邮箱", max_length=50, null=True)
    loginPW = models.CharField(verbose_name="登录密码", max_length=50)
    status = models.IntegerField(verbose_name="状态", choices=((0, "失效"), (1, "正常"), (2, "冻结")), default=1)
