import datetime
from django.contrib import auth
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User
from project.models import Project, Product, Progress, Vision, Task


# Create your views here.


# 登录界面
def login(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            username == User.objects.get(username=username).username  # 判断用户是否存在
        except User.DoesNotExist:
            context = {'wrong': '账号不存在'}
        else:
            user = auth.authenticate(request, username=username, password=password)  # 账户校验
            #  if check_password(password, User.objects.get(username=username).password):  # 密码校验
            if user:
                auth.login(request, user)
                return render(request, 'login/homepage.html', context)
            else:
                context = {'wrong': '密码不正确'}
    return render(request, 'login/login.html', context)


def homepage(request):
    now = datetime.date.today()
    if now.weekday() == 6:
        date = now-datetime.timedelta(days=2)  # 周日显示周五未填写进度
    elif now.weekday() == 0:
        date = now-datetime.timedelta(days=3)  # 周一显示上周五未填写进度
    else:
        date = now-datetime.timedelta(days=1)  # 显示昨天未填写进度
    # 查询未完成及未填写进度的任务
    task_list = Task.objects.filter(Q(task_status__in=['未开始', '进行中']) & ~Q(to_progress__date=date))
    page = request.GET.get('page', 1)
    # detail = request.GET.get('detail', '')
    # if detail:
    #     task_list = Task.objects.filter(products__product_model=detail)
    # else:
    #     task_list = Task.objects.all()  # 查询全部数据

    count_page = 10  # 按每页count_page条数据分页
    paginator = Paginator(task_list, count_page)
    start = (int(page) - 1) * count_page
    try:
        task_data = paginator.page(page)
    # 显示第一页,传入page的值为None或空，默认为1
    except PageNotAnInteger:
        task_data = paginator.page(1)
    # 传入page值不在有效范围
    except EmptyPage:
        task_data = paginator.page(paginator.num_pages)
    context = {
        'task_data': task_data,
        'start': start,
        'username': request.user.first_name,
        'date': date,
    }
    return render(request, 'login/homepage.html', context)

