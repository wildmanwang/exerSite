# Generated by Django 3.0.1 on 2020-04-11 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeinfo',
            name='email',
            field=models.CharField(max_length=50, null=True, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='employeeinfo',
            name='mobile',
            field=models.CharField(max_length=20, null=True, verbose_name='手机号码'),
        ),
    ]
