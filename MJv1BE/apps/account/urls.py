from django.urls import path
from . import views  # 导入视图

urlpatterns = [
    path('login/', views.login, name='login'),  # 登录视图
    path('enroll/', views.enroll, name='register'),  # 注册视图
    path('logout/', views.logout, name='logout'),  # 登出视图
    path('add_employee/', views.add_employee, name='add_employee'),
    path('refresh_token/', views.refresh_token, name='refresh_token'),
    path('get_userRole/', views.get_userRole, name='get_userRole'),
    path('reset_password/', views.reset_password, name='reset_password'),
]