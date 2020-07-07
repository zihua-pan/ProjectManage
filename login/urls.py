from django.urls import path
from . import views


app_name = 'login'
urlpatterns = [
    path('', views.login, name="login"),
    path('homepage/', views.homepage, name="homepage"),
    path('test/', views.test, name="test"),
]