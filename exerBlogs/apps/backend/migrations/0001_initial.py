# Generated by Django 3.0.1 on 2020-03-02 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='areaLever',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lever', models.IntegerField(choices=[(1, '省'), (2, '市'), (3, '县/区'), (4, '镇/街道')], verbose_name='级别')),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
                ('remark', models.TextField(null=True, verbose_name='备注')),
                ('super', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.areaLever', verbose_name='上级')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, verbose_name='用户名')),
                ('nickname', models.CharField(max_length=50, verbose_name='昵称')),
                ('mobile', models.CharField(max_length=20, verbose_name='手机号码')),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='电子邮箱')),
                ('password', models.CharField(max_length=50, verbose_name='密码')),
                ('userStatus', models.IntegerField(choices=[(0, '无效'), (1, '正常')], verbose_name='用户状态')),
                ('openBlog', models.IntegerField(choices=[(0, '未开放'), (1, '已开放'), (2, '临时封号'), (3, '主动停号'), (9, '永久封号')], default=0, verbose_name='博客状态')),
                ('blogAddress', models.CharField(max_length=50, null=True, verbose_name='博客域名')),
                ('blogSkin', models.CharField(default='default', max_length=50, verbose_name='博客皮肤')),
                ('name', models.CharField(max_length=50, null=True, verbose_name='姓名')),
                ('gender', models.IntegerField(choices=[(0, '女'), (1, '男')], null=True, verbose_name='性别')),
                ('birthdate', models.DateField(null=True, verbose_name='出生日期')),
                ('marriage', models.IntegerField(choices=[(1, '单身'), (2, '热恋'), (3, '订婚'), (4, '已婚'), (9, '离异')], null=True, verbose_name='婚姻状况')),
                ('position', models.CharField(max_length=50, null=True, verbose_name='职位')),
                ('company', models.CharField(max_length=50, null=True, verbose_name='单位')),
                ('work', models.IntegerField(choices=[(1, '学生'), (2, '待业'), (3, '就业'), (9, '其他')], null=True, verbose_name='工作状况')),
                ('homeCity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='homeCity', to='backend.areaLever', verbose_name='家乡城市')),
                ('homeProvince', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='homeProvince', to='backend.areaLever', verbose_name='家乡省份')),
                ('liveCity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='liveCity', to='backend.areaLever', verbose_name='城市')),
                ('liveProvince', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='liveProvince', to='backend.areaLever', verbose_name='省份')),
            ],
        ),
    ]
