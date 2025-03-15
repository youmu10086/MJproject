"""
URL configuration for MJv1BE project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views. Home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apartment import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customer/', views.get_customer),
    path('customer/query/', views.query_customer),
    path('customer/update/', views.update_customer),
    path('customer/add/', views.add_customer),
    path('customer/delete/', views.delete_customer),
    path('customers/delete/', views.delete_customers),
    path('upload/', views.upload),  # 上传文件
    path('room/', views.get_room),
    path('enroll/', views.enroll),
    path('login/', views.login),
    path('logout', views.logout),
]

# 允许media里所有文件被访问
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
