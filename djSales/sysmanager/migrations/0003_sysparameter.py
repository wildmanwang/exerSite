# Generated by Django 3.0.1 on 2020-01-27 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sysmanager', '0002_users_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='sysParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='参数名')),
                ('paraClass', models.CharField(max_length=20, verbose_name='分类')),
                ('describe', models.CharField(max_length=255, null=True, verbose_name='参数说明')),
                ('value', models.CharField(max_length=255, verbose_name='参数值')),
            ],
        ),
    ]
