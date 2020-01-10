from django.db import models

# Create your models here.


class Department(models.Model):
    name = models.CharField(verbose_name="名称", max_length=4)
    remark = models.CharField(verbose_name="备注", max_length=64, null=True)


class Project(models.Model):
    name = models.CharField(verbose_name="名称", max_length=64)


class Employee(models.Model):
    jobNumber = models.CharField(verbose_name="工号", max_length=16, unique=True)
    name = models.CharField(verbose_name="姓名", max_length=32)
    gender = models.IntegerField(verbose_name="性别", choices=((1, "男"), (0, "女")))
    dept = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)
    position = models.CharField(verbose_name="岗位", choices=(("product", "产品"), ("develop", "研发"), ("test", "测试"), ("service", "营运")), max_length=20, null=True)
    email = models.EmailField(verbose_name="电子邮箱", null=True)
    phone = models.CharField(verbose_name="手机号码", max_length=20, null=True)
    pwd = models.CharField(verbose_name="登录密码", max_length=32, null=True)
    rPro = models.ManyToManyField(to="Project")
    status=models.IntegerField(verbose_name="状态", choices=((0, "离职"), (1, "在职")), default=1)
