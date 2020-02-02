from django.db import models

# Create your models here.

class sysParameter(models.Model):
    name = models.CharField(verbose_name="参数名", max_length=50)
    paraClass = models.CharField(verbose_name="分类", max_length=20)
    describe = models.CharField(verbose_name="参数说明", max_length=255, null=True)
    value = models.CharField(verbose_name="参数值", max_length=255)

class Users(models.Model):
    name = models.CharField(verbose_name="用户名", max_length=20)
    mobileNumber = models.CharField(verbose_name="手机号码", max_length=20)
    email = models.CharField(verbose_name="电子邮箱", max_length=50)
    password = models.CharField(verbose_name="登录密码", max_length=50, null=True)
    status = models.IntegerField(verbose_name="状态", choices=((0, "无效"), (1, "正常")))

class Products(models.Model):
    code = models.CharField(verbose_name="编码", max_length=20)
    name = models.CharField(verbose_name="名称", max_length=50)
    price = models.DecimalField(verbose_name="参考价格", default=0.00, max_digits=10, decimal_places=2)
    verMain = models.CharField(verbose_name="主版本号", max_length=20, null=True)
    verSub = models.CharField(verbose_name="最新版本号", max_length=20, null=True)
    datePro = models.DateField(verbose_name="产品注册日期", null=True)
    dateCur = models.DateField(verbose_name="版本发布日期", null=True)
    status = models.IntegerField(verbose_name="状态", choices=((1, "正常"), (0, "下架")), default=1)
    remark = models.CharField(verbose_name="备注", max_length=255, null=True)

class Customer(models.Model):
    code = models.CharField(verbose_name="编码", max_length=20)
    name = models.CharField(verbose_name="名称", max_length=50)
    simpleName = models.CharField(verbose_name="简称", max_length=50)
    address = models.CharField(verbose_name="公司地址", max_length=255, null=True)
    contactPerson = models.ForeignKey("CusEmployee", null=True, on_delete=models.SET_NULL)
    products = models.ManyToManyField("Products")
    status = models.IntegerField(verbose_name="状态", choices=((1, "正常"), (0, "失效")), default=1)
    remark = models.CharField(verbose_name="备注", max_length=255, null=True)

class CusEmployee(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=20)
    curCustomer = models.ForeignKey("Customer", null=True, on_delete=models.SET_NULL)
    position = models.CharField(verbose_name="职位", max_length=20, null=True)
    mobile = models.CharField(verbose_name="手机号码", max_length=20, null=True)
    email = models.CharField(verbose_name="电子邮箱", max_length=50, null=True)
    status = models.IntegerField(verbose_name="状态", choices=((1, "正常"), (0, "失效")), default=1)
    remark = models.CharField(verbose_name="备注", max_length=255, null=True)