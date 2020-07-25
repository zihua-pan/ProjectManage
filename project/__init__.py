from django.apps import AppConfig
import os


default_app_config = 'project.ProjectConfig'


def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]


class ProjectConfig(AppConfig):
    name = get_current_app_name(__file__)  # 这里的结果是：project
    verbose_name = '项目管理'
