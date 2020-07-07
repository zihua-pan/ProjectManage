from django.shortcuts import render
from .models import User


# Create your views here.


def login(request):
    context = {}
    if request.method == 'POST':
        account = request.POST['account']
        password = request.POST['password']
        try:
            account == User.objects.get(account=account).account
        except User.DoesNotExist:
            context = {'wrong': '账号不存在'}
        else:
            if password == User.objects.get(account=account).password:
                return render(request, 'login/homepage.html', context)
            else:
                context = {'wrong': '密码不正确'}
    return render(request, 'login/login.html', context)


def homepage(request):
    return render(request, 'login/homepage.html')


def test(request):
    return render(request, 'login/test.html')