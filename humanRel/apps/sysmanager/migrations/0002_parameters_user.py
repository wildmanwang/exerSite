# Generated by Django 3.0.1 on 2020-02-16 07:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sysmanager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='parameters',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='parametersUser', to='sysmanager.User', verbose_name='用户'),
        ),
    ]
