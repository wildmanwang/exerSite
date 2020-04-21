# Generated by Django 3.0.1 on 2020-04-11 04:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssetType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='名称')),
            ],
            options={
                'verbose_name_plural': '设备类型表',
                'db_table': 'assettype',
            },
        ),
        migrations.CreateModel(
            name='BusinessUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='名称')),
            ],
            options={
                'verbose_name_plural': '业务线表',
                'db_table': 'businessunit',
            },
        ),
        migrations.CreateModel(
            name='EmployeeInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='姓名')),
                ('mobile', models.CharField(max_length=20, verbose_name='手机号码')),
                ('email', models.CharField(max_length=50, verbose_name='email')),
            ],
            options={
                'verbose_name_plural': '员工表',
                'db_table': 'employeeinfo',
            },
        ),
        migrations.CreateModel(
            name='Idc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='名称')),
                ('floor', models.IntegerField(verbose_name='楼层')),
            ],
            options={
                'verbose_name_plural': '机房表',
                'db_table': 'idc',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=20, verbose_name='名称')),
            ],
            options={
                'verbose_name_plural': '资产标签',
                'db_table': 'tag',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, verbose_name='用户名')),
                ('password', models.CharField(max_length=20, verbose_name='密码')),
                ('user_status_id', models.IntegerField(choices=[(1, '正常'), (0, '禁用')], verbose_name='状态')),
            ],
            options={
                'verbose_name_plural': '用户表',
                'db_table': 'userinfo',
            },
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cabinet_num', models.CharField(blank=True, max_length=30, null=True, verbose_name='机柜号')),
                ('cabinet_order', models.CharField(blank=True, max_length=30, null=True, verbose_name='机柜中序号')),
                ('remark', models.CharField(max_length=50, null=True, verbose_name='备注')),
                ('device_status_id', models.IntegerField(choices=[(1, '上架'), (2, '上线'), (3, '离线'), (4, '下架')], default=1, verbose_name='设备状态')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(blank=True, null=True)),
                ('business_unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='businessunit', to='web.BusinessUnit', verbose_name='业务线')),
                ('device_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assetType', to='web.AssetType', verbose_name='设备类型')),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employeeinfo', to='web.EmployeeInfo', verbose_name='员工')),
                ('idc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='idc', to='web.Idc', verbose_name='机房')),
                ('tag', models.ManyToManyField(to='web.Tag')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='userinfo', to='web.UserInfo', verbose_name='用户')),
            ],
            options={
                'verbose_name_plural': '资产表',
                'db_table': 'asset',
            },
        ),
    ]