from django.contrib.auth.models import Group
from django.shortcuts import render
from login.models import User

# Create your views here.


# 用户信息
def user(request):
    if User.objects.count() == 0:  # 如果没有用户
        context = {
            'wrong': '暂无数据',
        }
    else:
        context = {
            'userset': User.objects.all(),
            'username': request.user.first_name,
        }
    return render(request, 'system/user.html', context)


# 角色信息
def role(request):
    admin_set = Group.objects.get(id=1).user_set.all()  # 所有管理员角色用户
    leader_set = Group.objects.get(id=2).user_set.all()  # 所有组长角色用户
    member_set = Group.objects.get(id=3).user_set.all()  # 所有组员角色用户
    context = {
        'admin_set': admin_set,
        'leader_set': leader_set,
        'member_set': member_set,
        'username': request.user.first_name,
    }
    return render(request, 'system/role.html', context)
