from django import forms
from django.forms import widgets
from .models import User
from django.core.exceptions import ValidationError
from django.shortcuts import render


'''
class UserForm(forms.Form):
    account = forms.CharField(min_length=2, label='', widget=widgets.TextInput({'placeholder': "账号"}),
                              error_messages={
                                  'required': '账号不能为空',
                                  'notexist': '账号不存在',
                                  'min_length': '222222'
                                             })
    password = forms.CharField(min_length=2, label='',widget=widgets.TextInput({'placeholder': "密码"}),
                               error_messages={
                                   'required': '密码不能为空',
                               })

    def clean_account(self):
        account = self.cleaned_data.get('account')
        try:
            account = User.objects.get(account=account).account
        except User.DoesNotExist:
            return render()
        else:
            return account




    def clean(self):
        account = self.cleaned_data.get('account')
        password = self.cleaned_data.get('password')
        if password == User.objects.get(account=account).password:
            return self.cleaned_data
        else:
            raise ValidationError('密码错误')
'''

