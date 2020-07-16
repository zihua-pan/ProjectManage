from django.urls import path
from . import views


app_name = 'system'
urlpatterns = [
    path('user/', views.user, name='user'),
    path('role/', views.role, name='role'),
    path('base/', views.base, name='base'),
]