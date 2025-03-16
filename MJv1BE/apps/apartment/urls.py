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
    path('room/', views.get_room, name='room'),  # 对应 'room/'
]