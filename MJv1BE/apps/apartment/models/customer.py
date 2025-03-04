# apps/apartment/models/customer.py
from django.db import models

class Customer(models.Model):
    gender_choice = (('男', '男'), ('女', '女'))
    cno = models.CharField(db_column='Cno', primary_key=True, null=False, max_length=100)
    name = models.CharField(db_column='CName', max_length=100, null=False)
    gender = models.CharField(db_column='Gender', choices=gender_choice, max_length=20, null=False)
    mobile = models.CharField(db_column='Mobile', max_length=20, null=False)
    roomNo = models.CharField(db_column='RoomNo', max_length=20, null=False)
    checkInTime = models.DateTimeField(db_column='CheckInTime', null=False)
    checkOutTime = models.DateTimeField(db_column='CheckOutTime', null=True)
    resideTimePeriod = models.CharField(db_column='resideTimePeriod',max_length=100, null=False)
    idCardNo = models.CharField(db_column='IDCardNo', max_length=20, null=False)
    image = models.CharField(db_column='Image', max_length=100, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, db_column='Balance')


    class Meta:
        managed = True
        db_table = 'customer'
        app_label = 'apartment'

    def __str__(self):
        return '序号：%s\t姓名：%s\t房间号：%s\t' % (self.cno, self.name, self.roomNo)