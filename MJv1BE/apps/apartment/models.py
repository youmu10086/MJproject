from django.db import models

from account.models import CustomUser


class RoomConfig(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="配置名称")
    description = models.TextField(null=True, blank=True, verbose_name="配置描述")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "room_config"
        verbose_name = "房间配置项"
        verbose_name_plural = "房间配置项"


class Room(models.Model):
    status_choices = (("vacant", "空闲"), ("occupied", "已入住"), ("maintenance", "维护中"), ("reserved", "已预订"),
                      ("cleaning", "清洁中"), ("locked", "锁定"), ("unavailable", "不可用"))
    room_no = models.CharField(max_length=10, primary_key=True, verbose_name="房间号")
    room_status = models.CharField(max_length=20, choices=status_choices, default="vacant", verbose_name="房间状态")
    room_type = models.CharField(max_length=50, verbose_name="房间类型")
    room_amount = models.DecimalField(decimal_places=2, max_digits=10, verbose_name="房间金额")
    duration_type = models.CharField(max_length=20, null=True, blank=True, verbose_name="租住时间单位")
    room_config = models.ManyToManyField(RoomConfig, related_name="rooms", verbose_name="房间配置")

    def __str__(self):
        return f"房间 {self.room_no}"

    class Meta:
        db_table = "room"
        verbose_name = "房间"
        verbose_name_plural = "房间"


class Customer(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        db_column='room_id',
        db_constraint=True,
        to_field='room_no'  # 明确指定关联字段
    )
    gender_choice = (('男', '男'), ('女', '女'))
    status_choice = (
    ('已预订', '已预订'), ('已入住', '已入住'), ('已退宿', '已退宿'), ('未知', '未知'), ('已取消预订', '已取消预订'))
    cno = models.CharField(db_column='Cno', primary_key=True, null=False, max_length=100)
    name = models.CharField(db_column='CName', max_length=100, null=False)
    gender = models.CharField(db_column='Gender', choices=gender_choice, max_length=20, null=False)
    mobile = models.CharField(db_column='Mobile', max_length=20, null=False)
    checkInTime = models.DateTimeField(db_column='CheckInTime', null=False)
    checkOutTime = models.DateTimeField(db_column='CheckOutTime', null=True)
    resideTimePeriod = models.CharField(db_column='resideTimePeriod', max_length=100, null=False)
    idCardNo = models.CharField(db_column='IDCardNo', max_length=20, null=False)
    image = models.CharField(db_column='Image', max_length=100, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, db_column='Balance', default=0)
    status = models.CharField(db_column='Status', choices=status_choice, max_length=20, null=False, default='未知')
    # rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, db_column='Rate', default=5)
    user = models.ForeignKey(
        CustomUser,  # 使用你的自定义用户模型
        on_delete=models.CASCADE,  # 用户删除时，关联的客户记录也被删除
        db_column='user_id',  # 数据库列名
        null=True,  # 允许未登录用户创建的客户记录（根据需求调整）
        blank=True,  # 允许表单中不填写
        verbose_name='关联用户',
        related_name='customers'  # 反向查询名称（user.customers.all()）
    )

    class Meta:
        managed = True
        db_table = 'customer'
        app_label = 'apartment'

    def __str__(self):
        return '序号：%s\t姓名：%s\t房间号：%s\t' % (self.cno, self.name, self.room.room_no)
