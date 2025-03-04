# apps/apartment/models/room.py
from django.db import models

class Room(models.Model):
    roomNo = models.CharField(db_column='RoomNo', max_length=20, primary_key=True)
    roomAmount = models.DecimalField(db_column='RoomAmount', decimal_places=2, max_digits=10)
    durationType = models.CharField(db_column='DurationType', max_length=20, null=True)
    roomType = models.CharField(db_column='RoomType', max_length=20, null=True)

    class Meta:
        managed = True
        db_table = 'room'
        app_label = 'apartment'

    def __str__(self):
        return '房间号：%s\t金额：%s\t' % (self.roomNo, self.roomAmount)