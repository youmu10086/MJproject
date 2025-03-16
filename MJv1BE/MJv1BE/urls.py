from django.conf import settings  
from django.conf.urls.static import static  
from django.contrib import admin  
from django.urls import path, include  # 包含 include  

urlpatterns = [  
    path('admin/', admin.site.urls),  

    # 包含 apartment 应用的 URL 配置  
    path('', include('apartment.urls')),  # customer 相关 URL

    # 包含 account 应用的 URL 配置  
    path('', include('account.urls')),  # 将所有 account 的 URL 引入，让其在根路径下可用  
]  

# 允许 media 目录下的所有文件被访问  
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  