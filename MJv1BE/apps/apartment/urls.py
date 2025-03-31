from django.urls import path
from . import views  # 导入视图

urlpatterns = [
    path('customer/', views.get_customer, name='customer'),  # 对应 'customer/' 的请求
    path('customer/query/', views.query_customer, name='query_customer'),  # 对应 'customer/query/'
    path('customer/update/', views.update_customer, name='update_customer'),  # 对应 'customer/update/'
    path('customer/add/', views.add_customer, name='add_customer'),  # 对应 'customer/add/'
    path('customer/delete/', views.delete_customer, name='delete_customer'),  # 对应 'customer/delete/'
    path('customers/delete/', views.delete_customers, name='delete_customers'),  # 对应 'customers/delete/'
    path('upload/', views.upload, name='upload'),  # 对应 'upload/'
    path('room/', views.get_room, name='room'),
    path('room/add/', views.add_room, name='add_room'),
    path('room/delete/', views.delete_room, name='delete_room'),
    path('room/update/', views.update_room, name='update_room'),
    path('room/config/', views.get_room_config, name='config_room'),
    path('room/config/add/', views.add_room_config, name='add_room_config'),
    path('room/config/delete/', views.delete_room_config, name='delete_room_config'),
]