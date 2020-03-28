from django.db import models

# Create your models here.
class Blog(models.Model):
    title = models.CharField(verbose_name="标题", max_length=128)
    owner = models.ForeignKey(verbose_name="作者", to="backend.User", related_name="blogOwner", null=True, on_delete=models.SET_NULL)
    contents = models.TextField(verbose_name="内容")
    createTime = models.DateTimeField(verbose_name="新建时间")
    updateTime = models.DateTimeField(verbose_name="更新时间", null=True)
    upTimes = models.IntegerField(verbose_name="点赞数", default=0)


class BlogUpRecord(models.Model):
    blog = models.ForeignKey(verbose_name="博客", to="Blog", related_name="upBlog", on_delete=models.CASCADE)
    upUser = models.ForeignKey(verbose_name="点赞人", to="backend.User", related_name="upUser", on_delete=models.DO_NOTHING)
