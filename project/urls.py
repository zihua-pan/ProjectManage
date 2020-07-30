from django.urls import path
from . import views


app_name = 'project'
urlpatterns = [
    # 产品相关url
    path('product/', views.product, name='product'),
    path('product/download/', views.download_product, name='download_product'),
    path('product/add/', views.product_add, name='product_add'),
    path('product/modify/', views.product_modify, name='product_modify'),

    # 项目相关url
    path('project/', views.project, name='project'),
    path('project/download/', views.project_download, name='project_download'),
    path('project/add/', views.project_add, name='project_add'),
    path('project/modify/', views.project_modify, name='project_modify'),

    # 任务相关url
    path('task/', views.task, name='task'),

    # 版本相关url
    path('vision/', views.vision, name='vision'),

    # 进度相关url
    path('progress/', views.progress, name='progress'),

]
