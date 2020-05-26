from django.urls import path
from . import views


app_name = 'project'
urlpatterns = [
    path('product/', views.product, name='product'),
    path('project/', views.project, name='project'),
    path('task/', views.task, name='task'),
    path('vision/', views.vision, name='vision'),
    path('progress/', views.progress, name='progress'),
    path('product/download/', views.download, name='download'),
    path('product/delete/', views.delete, name='delete'),
]
