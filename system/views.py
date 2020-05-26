from django.shortcuts import render
from login.models import User

# Create your views here.


def user(request):
    if User.objects.count() == 0:
        context = {
            'wrong': '暂无数据',
        }
    else:
        #将所有数据打包成列表传递到前端
        context = {
            'userset': list(User.objects.all()),
        }
    return render(request, 'system/user.html', context)


def role(request):
    if User.objects.count() == 0:
        context = {
            'wrong': '暂无数据',
        }
    else:
        #将不同角色数据打包成列表传到前端
        context = {
            'mg_user': list(User.objects.filter(role='管理员')),
            'gl_user': list(User.objects.filter(role='组长')),
            'mb_user': list(User.objects.filter(role='成员')),
        }
    return render(request, 'system/role.html', context)


def base(request):
    return render(request, 'system/base.html')