from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    area = models.CharField(max_length=20, verbose_name='地区')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        ordering = ['id']




