from django.contrib import admin
from .models import Customer, Room


# 注册模型
admin.site.register(Customer)
admin.site.register(Room)