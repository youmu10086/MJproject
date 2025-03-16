from django.urls import path
from . import views  # 导入视图

urlpatterns = [
    path('login/', views.login, name='login'),  # 登录视图
    path('enroll/', views.enroll, name='register'),  # 注册视图
    path('logout/', views.logout, name='logout'),  # 登出视图
]