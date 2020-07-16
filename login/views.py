from django.contrib import auth
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User


# Create your views here.



#登录界面
def login(request):
    context = {}
    print('1================1')
    print(request.user)
    print('1=================1')
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
                print('2================2')
                print(request.user)
                print('2=================2')
                return render(request, 'login/homepage.html', context)
            else:
                context = {'wrong': '密码不正确'}
    return render(request, 'login/login.html', context)


def homepage(request):
    return render(request, 'login/homepage.html')


def test(request):
    return render(request, 'login/test.html')