from django.db import models


class UserInfo(models.Model):
    """
    用户表
    """
    username = models.CharField(verbose_name="用户名", max_length=20)
    password = models.CharField(verbose_name="密码", max_length=20)
    user_status_id = models.IntegerField(verbose_name="状态", choices=((1, "正常"), (0, "禁用")))

    class Meta:
        verbose_name_plural = "用户表"
        db_table = "userinfo"

    def __str__(self):
        return self.username


class EmployeeInfo(models.Model):
    """
    员工表
    """
    name = models.CharField(verbose_name="姓名", max_length=20)
    mobile = models.CharField(verbose_name="手机号码", max_length=20, null=True)
    email = models.CharField(verbose_name="email", max_length=50, null=True)

    class Meta:
        verbose_name_plural = "员工表"
        db_table = "employeeinfo"

    def __str__(self):
        return self.name


class BusinessUnit(models.Model):
    """
    业务线表
    """
    name = models.CharField(verbose_name="名称", max_length=40)

    class Meta:
        verbose_name_plural = "业务线表"
        db_table = "businessunit"

    def __str__(self):
        return self.name


class Idc(models.Model):
    """
    机房表
    """
    name = models.CharField(verbose_name="名称", max_length=20)
    floor = models.IntegerField(verbose_name="楼层")

    class Meta:
        verbose_name_plural = "机房表"
        db_table = "idc"

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    资产标签
    """
    caption = models.CharField(verbose_name="名称", max_length=20)

    class Meta:
        verbose_name_plural = "资产标签"
        db_table = "tag"

    def __str__(self):
        return self.caption


class AssetType(models.Model):
    """
    设备类型
    """
    name = models.CharField(verbose_name="名称", max_length=20)

    class Meta:
        verbose_name_plural = "设备类型表"
        db_table = "assettype"

    def __str__(self):
        return self.name


class Asset(models.Model):
    """
    设备表
    """
    device_status_choices = (
        (1, "上架"),
        (2, "上线"),
        (3, "离线"),
        (4, "下架"),
    )
    device_type = models.ForeignKey(verbose_name="设备类型", to="AssetType", related_name="assetType", null=True, on_delete=models.SET_NULL)
    business_unit = models.ForeignKey(verbose_name="业务线", to="BusinessUnit", related_name="businessunit", null=True, on_delete=models.SET_NULL)
    employee = models.ForeignKey(verbose_name="员工", to="EmployeeInfo", related_name="employeeinfo", null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(verbose_name="用户", to="UserInfo", related_name="userinfo", null=True, on_delete=models.SET_NULL)
    idc = models.ForeignKey(verbose_name="机房", to="Idc", related_name="idc", null=True, on_delete=models.SET_NULL)
    tag = models.ManyToManyField(to="Tag")

    cabinet_num = models.CharField(verbose_name="机柜号", max_length=30, null=True, blank=True)
    cabinet_order = models.CharField(verbose_name="机柜中序号", max_length=30, null=True, blank=True)

    remark = models.CharField(verbose_name="备注", max_length=50, null=True)
    device_status_id = models.IntegerField(verbose_name="设备状态", choices=device_status_choices, default=1)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "资产表"
        db_table = "asset"

    def __str__(self):
        return "{name}-{num}-{order}".format(name=self.idc.name, num=self.cabinet_num, order=self.cabinet_order)
