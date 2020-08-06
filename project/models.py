from django.db import models
from django.utils import timezone

# Create your models here.


# 项目表
class Project(models.Model):
    project_num = models.CharField(max_length=30, unique=True, primary_key=True, verbose_name='项目编号')
    project_name = models.CharField(max_length=30, verbose_name='项目名称')
    project_manager = models.CharField(max_length=20, verbose_name='项目经理')
    create_time = models.DateTimeField(auto_now_add=timezone.now, verbose_name='创建时间')

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = '项目'


# 事业部表
class Department(models.Model):
    department_name = models.CharField(max_length=20, unique=True, primary_key=True, verbose_name='事业部')
    projects = models.ManyToManyField(
        Project,
        related_name='to_department',
        verbose_name='项目编号',)

    class Meta:
        verbose_name = '事业部'
        verbose_name_plural = '事业部'


# 产品表
class Product(models.Model):
    projects = models.ForeignKey(
        Project,
        to_field='project_num',
        on_delete=models.CASCADE,
        related_name='to_product',
        verbose_name='所属项目', )
    product_model = models.CharField(max_length=30, unique=True, primary_key=True, verbose_name='产品型号')
    product_name = models.CharField(max_length=30, verbose_name='产品名称')
    product_type = models.CharField(max_length=20, verbose_name='产品类型')
    create_time = models.DateTimeField(auto_now_add=timezone.now, verbose_name='创建时间')

    class Meta:
        verbose_name = '产品'
        verbose_name_plural = '产品'
        ordering = ['-create_time']


# 任务表
class Task(models.Model):
    # 任务状态备选项
    status_choice = (
        ('no', '未开始'),
        ('doing', '进行中'),
        ('done', '已完成'),
    )
    products = models.ForeignKey(
        Product,
        to_field='product_model',
        on_delete=models.CASCADE,
        related_name='to_task',
        verbose_name='所属产品',)
    task_num = models.CharField(max_length=20, unique=True, primary_key=True, verbose_name='任务单号')
    dev_type = models.CharField(max_length=20, verbose_name='开发类型')
    start_time = models.DateField(blank=True, null=True, verbose_name='开始时间')
    end_time = models.DateField(blank=True, null=True, verbose_name='结束时间')
    task_status = models.CharField(max_length=10, choices=status_choice, verbose_name='任务状态')
    create_time = models.DateTimeField(auto_now_add=timezone.now, verbose_name='创建时间')

    class Meta:
        ordering = ['-task_num']
        verbose_name = '任务'
        verbose_name_plural = '任务'


# 版本表
class Vision(models.Model):
    tasks = models.ForeignKey(
        Task,
        to_field='task_num',
        on_delete=models.CASCADE,
        related_name='to_vision',
        verbose_name='所属任务',)
    vision_num = models.PositiveIntegerField(verbose_name='版本数')
    vision_name = models.CharField(max_length=40,  primary_key=True, verbose_name='版本名称')
    executor = models.CharField(max_length=20, verbose_name='执行人')
    start_time = models.DateField(blank=True, verbose_name='开始时间')
    end_time = models.DateField(blank=True, verbose_name='结束时间')
    create_time = models.DateTimeField(auto_now_add=timezone.now, verbose_name='创建时间')

    class Meta:
        ordering = ['vision_num']
        verbose_name = '版本'
        verbose_name_plural = '版本'


# 进度表
class Progress(models.Model):
    tasks = models.ForeignKey(
        Task,
        to_field='task_num',
        on_delete=models.CASCADE,
        related_name='to_progress',
        verbose_name='所属任务',)
    date = models.DateField(verbose_name='日期')
    executor = models.CharField(max_length=20, verbose_name='执行人')
    hours = models.FloatField(verbose_name='工时')
    record = models.TextField(verbose_name='开发记录')
    create_time = models.DateTimeField(auto_now_add=timezone.now, verbose_name='创建时间')

    class Meta:
        ordering = ['-date']
        verbose_name = '进度'
        verbose_name_plural = '进度'

