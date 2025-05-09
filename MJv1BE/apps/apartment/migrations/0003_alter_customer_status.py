# Generated by Django 5.1.7 on 2025-05-04 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0002_customer_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='status',
            field=models.CharField(choices=[('已预订', '已预订'), ('已入住', '已入住'), ('已退宿', '已退宿'), ('未知', '未知'), ('已取消预订', '已取消预订')], db_column='Status', default='未知', max_length=20),
        ),
    ]
