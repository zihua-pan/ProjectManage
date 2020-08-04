from django.urls import path
from . import views


app_name = 'project'
urlpatterns = [
    # 产品相关url
    path('product/', views.product, name='product'),
    path('product/download/<int:model>', views.product_download, name='product_download'),
    path('product/import/', views.product_import, name='product_import'),
    path('product/add/', views.product_add, name='product_add'),
    path('product/modify/', views.product_modify, name='product_modify'),

    # 项目相关url
    path('project/', views.project, name='project'),
    path('project/download/<int:model>', views.project_download, name='project_download'),
    path('project/import/', views.project_import, name='project_import'),
    path('project/add/', views.project_add, name='project_add'),
    path('project/modify/', views.project_modify, name='project_modify'),

    # 任务相关url
    path('task/', views.task, name='task'),
    path('task/download/<int:model>', views.task_download, name='task_download'),
    path('task/import/', views.task_import, name='task_import'),
    path('task/add/', views.task_add, name='task_add'),
    path('task/modify/', views.task_modify, name='task_modify'),

    # 版本相关url
    path('vision/', views.vision, name='vision'),
    path('vision/download/<int:model>', views.vision_download, name='vision_download'),
    path('vision/import/', views.vision_import, name='vision_import'),
    path('vision/add/', views.vision_add, name='vision_add'),
    path('vision/modify/', views.vision_modify, name='vision_modify'),

    # 进度相关url
    path('progress/', views.progress, name='progress'),
    path('progress/download/<int:model>', views.progress_download, name='progress_download'),
    path('progress/import/', views.progress_import, name='progress_import'),
    path('progress/add/', views.progress_add, name='progress_add'),
    path('progress/modify/', views.progress_modify, name='progress_modify'),
]
