from django.db import models

# Create your models here.


class User(models.Model):
    account = models.CharField(max_length=20, verbose_name='账户')
    username = models.CharField(max_length=10, verbose_name='姓名')
    password = models.CharField(max_length=20, verbose_name='密码')
    area = models.CharField(max_length=20, verbose_name='地区')
    role = models.CharField(max_length=10, verbose_name='角色')
    email = models.EmailField(blank=True, verbose_name='邮箱')
    create_time = models.DateTimeField(verbose_name='创建时间')


