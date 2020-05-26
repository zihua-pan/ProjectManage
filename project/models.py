from django.db import models


# Create your models here.


class Product(models.Model):
    pd_model = models.CharField(max_length=20, verbose_name='产品型号')
    pd_type = models.CharField(max_length=20, verbose_name='产品类型')
    pd_name = models.CharField(max_length=20, verbose_name='产品名称')


class Project(models.Model):
    pj_num = models.CharField(max_length=20, verbose_name='项目编号')
    pj_name = models.CharField(max_length=20, verbose_name='项目名称')
    pd_model = models.CharField(max_length=20, verbose_name='产品型号')
    pj_manager = models.CharField(max_length=20, verbose_name='项目经理')
    bd = models.CharField(max_length=20, verbose_name='所属事业部')


class Task(models.Model):
    t_num = models.CharField(max_length=20, verbose_name='任务单号')
    pj_num_name = models.CharField(max_length=40, verbose_name='项目编号名称')
    pd_model = models.CharField(max_length=20, verbose_name='产品型号')
    dev_type = models.CharField(max_length=20, verbose_name='开发类型')
    s_time = models.CharField(max_length=20, verbose_name='开始时间')
    e_time = models.CharField(max_length=20, verbose_name='结束时间')
    t_status = models.CharField(max_length=10, verbose_name='任务状态')


class Vision(models.Model):
    t_num = models.CharField(max_length=20, verbose_name='任务单号')
    pj_num_name = models.CharField(max_length=40, verbose_name='项目编号名称')
    v_num = models.CharField(max_length=20, verbose_name='版本数')
    v_name = models.CharField(max_length=20, verbose_name='版本名称')
    executor = models.CharField(max_length=20, verbose_name='执行人')
    s_time = models.CharField(max_length=20, verbose_name='开始时间')
    e_time = models.CharField(max_length=20, verbose_name='结束时间')


class Progress(models.Model):
    t_num = models.CharField(max_length=20, verbose_name='任务单号')
    pj_num_name = models.CharField(max_length=40, verbose_name='项目编号名称')
    data = models.CharField(max_length=20, verbose_name='日期')
    pd_model = models.CharField(max_length=20, verbose_name='产品型号')
    executor = models.CharField(max_length=20, verbose_name='执行人')
    hours = models.CharField(max_length=20, verbose_name='工时')
    record = models.CharField(max_length=20, verbose_name='开发记录')