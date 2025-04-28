from django.contrib import admin
from .models import Room, RoomConfig, Customer


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_no', 'room_status', 'room_type', 'room_amount', 'duration_type')
    search_fields = ('room_no', 'room_type')
    list_filter = ('room_status',)
    ordering = ('room_no',)


@admin.register(RoomConfig)
class RoomConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'cno',
        'name',
        'gender',
        'mobile',
        'room_no',  # Modify to access the related Room's room_no
        'checkInTime',
        'checkOutTime'
    )
    search_fields = ('cno', 'name', 'mobile', 'room__room_no')  # Modify to access the related Room's room_no
    list_filter = ('gender', 'checkInTime')
    ordering = ('checkInTime',)

    def room_no(self, obj):  # Custom method to display the room number
        return obj.room.room_no if obj.room else '-'

    room_no.short_description = '房间号'  # Set a human-readable name for the method in the Admin
