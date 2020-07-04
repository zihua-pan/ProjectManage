from django.urls import path
from . import views


app_name = 'project'
urlpatterns = [
    path('product/', views.product, name='product'),
    path('product/download/', views.download, name='download'),
    path('product/add/', views.product_add, name='product_add'),

    path('project/', views.project, name='project'),
    path('task/', views.task, name='task'),
    path('vision/', views.vision, name='vision'),
    path('progress/', views.progress, name='progress'),

]
