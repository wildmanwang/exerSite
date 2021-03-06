# Generated by Django 3.0.1 on 2020-02-16 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseinfo', '0002_auto_20200216_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='education',
            field=models.IntegerField(choices=[(0, '在读'), (1, '小学'), (2, '初中'), (3, '高中'), (4, '大专'), (5, '本科'), (6, '硕士'), (7, '博士'), (99, '其他')], verbose_name='学历'),
        ),
        migrations.AlterField(
            model_name='person',
            name='relType',
            field=models.IntegerField(choices=[(0, '自己'), (1, '血亲'), (2, '姻亲'), (3, '同学'), (4, '朋友'), (5, '同事'), (6, '战友'), (7, '街坊'), (99, '其他')], verbose_name='关系类型'),
        ),
    ]
