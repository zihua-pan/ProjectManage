from django.urls import path
from . import views


app_name = 'project'
urlpatterns = [
    # 产品相关url
    path('product/', views.product, name='product'),
    path('product/download/', views.download_product, name='download_product'),
    path('product/add/', views.product_add, name='product_add'),

    # 项目相关url
    path('project/', views.project, name='project'),

    # 任务相关url
    path('task/', views.task, name='task'),

    # 版本相关url
    path('vision/', views.vision, name='vision'),

    # 进度相关url
    path('progress/', views.progress, name='progress'),

]
