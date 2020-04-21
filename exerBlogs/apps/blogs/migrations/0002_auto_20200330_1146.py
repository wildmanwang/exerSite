# Generated by Django 3.0.1 on 2020-03-30 03:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='article_type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=32, verbose_name='标题')),
            ],
        ),
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=32, verbose_name='标题')),
            ],
        ),
        migrations.AddField(
            model_name='blog',
            name='article_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blogs.article_type'),
        ),
        migrations.AddField(
            model_name='blog',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blogs.category'),
        ),
    ]