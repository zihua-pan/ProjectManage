from django.apps import AppConfig
import os


default_app_config = 'login.LoginConfig'


def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]


class LoginConfig(AppConfig):
    name = get_current_app_name(__file__)  # 这里的结果是：login
    verbose_name = '用户管理'
