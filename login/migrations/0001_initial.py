# Generated by Django 3.0.5 on 2020-05-18 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.CharField(max_length=20, verbose_name='账户')),
                ('username', models.CharField(max_length=10, verbose_name='姓名')),
                ('password', models.CharField(max_length=20)),
                ('area', models.CharField(max_length=20, verbose_name='地区')),
                ('role', models.CharField(max_length=10, verbose_name='角色')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='邮箱')),
                ('create_time', models.DateTimeField(verbose_name='创建时间')),
            ],
        ),
    ]
