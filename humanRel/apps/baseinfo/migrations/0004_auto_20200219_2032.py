# Generated by Django 3.0.1 on 2020-02-19 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseinfo', '0003_auto_20200216_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='relType',
            field=models.IntegerField(choices=[(0, '自己'), (1, '族亲'), (2, '姻亲'), (3, '同学'), (4, '朋友'), (5, '同事'), (6, '战友'), (7, '街坊'), (99, '其他')], verbose_name='关系类型'),
        ),
    ]