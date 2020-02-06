# Generated by Django 3.0.1 on 2020-01-23 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='用户名')),
                ('mobileNumber', models.CharField(max_length=20, verbose_name='手机号码')),
                ('email', models.CharField(max_length=50, verbose_name='电子邮箱')),
                ('status', models.IntegerField(choices=[(0, '无效'), (1, '正常')], verbose_name='状态')),
            ],
        ),
    ]