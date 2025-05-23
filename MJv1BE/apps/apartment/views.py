import traceback
from os import path, remove

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q, F  # 导入q查询
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.utils import json
from rest_framework_simplejwt.authentication import JWTAuthentication

from account.models import CustomUser
from .models import Customer, Room, RoomConfig
from .myTool import *
from .permissions import IsManager


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def get_room(request):
    try:
        rooms = Room.objects.prefetch_related('room_config').all()
        room_data = []
        for room in rooms:
            room_info = {
                'room_no': room.room_no,
                'room_status': room.room_status,
                'room_type': room.room_type,
                'room_amount': str(room.room_amount),  # DecimalField 需要转换为字符串
                'duration_type': room.duration_type,
                'room_config': [config.name for config in room.room_config.all()]  # 获取配置名称列表
            }
            room_data.append(room_info)

        return JsonResponse({'code': 1, 'data': room_data}, safe=False)
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': '获取房间信息时出现异常:' + str(e)})


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def get_room_config(request):
    try:
        room_configs = RoomConfig.objects.all().values('id', 'name', 'description')

        room_configs_list = list(room_configs)

        return JsonResponse({'code': 1, 'data': room_configs_list, 'msg': '获取房间配置成功'})

    except Exception as e:
        return JsonResponse({'code': 0, 'msg': f'获取房间配置出现异常: {str(e)}'}, status=500)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])  # 根据实际情况调整权限类
def add_room_config(request):
    try:
        data = request.data
        name = data.get('name')
        description = data.get('description')

        if not name:
            return JsonResponse({'code': 0, 'msg': '配置名称不能为空'}, status=400)

        # 检查是否已存在同名配置
        if RoomConfig.objects.filter(name=name).exists():
            return JsonResponse({'code': 0, 'msg': '配置名称已存在'}, status=400)

        RoomConfig.objects.create(name=name, description=description)
        return JsonResponse({'code': 1, 'msg': '添加房间配置成功'})

    except Exception as e:
        return JsonResponse({'code': 0, 'msg': f'添加房间配置出现异常: {str(e)}'}, status=500)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])  # 根据实际情况调整权限类
def delete_room_config(request):
    try:
        config_id = request.query_params.get('config_id')

        if not config_id:
            return JsonResponse({'code': 0, 'msg': '配置ID不能为空'}, status=400)

        room_config = RoomConfig.objects.filter(id=config_id).first()

        if not room_config:
            return JsonResponse({'code': 0, 'msg': '配置不存在'}, status=404)

        # 手动清理多对多关系
        rooms_with_config = Room.objects.filter(room_config=room_config)
        for room in rooms_with_config:
            room.room_config.remove(room_config)

        room_config.delete()
        return JsonResponse({'code': 1, 'msg': '删除房间配置成功'})

    except Exception as e:
        return JsonResponse({'code': 0, 'msg': f'删除房间配置出现异常: {str(e)}'}, status=500)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsManager])
@transaction.atomic  # 添加事务管理
def add_room(request):
    try:
        data = request.data  # 使用 DRF 的 request.data

        # 创建 Room 实例
        room = Room.objects.create(
            room_no=data['roomNo'],
            room_status='vacant',  # 默认状态，可以根据需要修改
            room_type=data['roomType'],
            room_amount=data['roomAmount'],
            duration_type=data.get('durationType', None)
        )

        # 处理多对多关系
        if 'roomConfig' in data:
            room_config_ids = data['roomConfig']
            room_configs = RoomConfig.objects.filter(id__in=room_config_ids)
            room.room_config.set(room_configs)

        rooms = Room.objects.all().values()
        rooms_list = list(rooms)
        return JsonResponse({'code': 1, 'data': rooms_list})

    except Exception as e:
        import traceback
        print(traceback.format_exc())  # 打印堆栈跟踪，仅在开发环境中使用
        return JsonResponse({'code': 0, 'msg': '添加房间出现异常: ' + str(e)})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsManager])
@transaction.atomic  # 添加事务管理
def update_room(request):
    try:
        # 安全获取数据
        data = request.data  # 使用 DRF 的 request.data
        required_fields = ['room_no', 'room_amount', 'room_type', 'room_config', 'duration_type', 'room_status']
        if not all(field in data for field in required_fields):
            return JsonResponse({'code': 0, 'msg': '缺少必要参数'}, status=400)

        obj_room = Room.objects.select_for_update().get(room_no=data['room_no'])
        obj_room.room_status = data['room_status']
        obj_room.room_amount = data['room_amount']
        obj_room.room_type = data['room_type']
        obj_room.duration_type = data['duration_type']

        # 获取前端传递的配置项名称列表
        config_names = data['room_config']
        if not isinstance(config_names, list):
            return JsonResponse({'code': 0, 'msg': '配置项格式错误'}, status=400)

        # 将配置项名称转换为 ID
        valid_config_ids = []
        invalid_names = []
        all_configs = {config.name: config.id for config in RoomConfig.objects.all()}  # 预取所有配置
        for name in config_names:
            if name in all_configs:
                valid_config_ids.append(all_configs[name])
            else:
                invalid_names.append(name)

        if invalid_names:
            return JsonResponse({'code': 0, 'msg': f'包含无效配置项: {invalid_names}'}, status=400)

        # 设置配置项
        obj_room.room_config.set(valid_config_ids)
        obj_room.save()

        # 返回更新后的房间信息
        rooms = Room.objects.prefetch_related('room_config').all().values(
            'room_no',
            'room_status',
            'room_type',
            'room_amount',
            'duration_type',
            room_configs=F('room_config__name')  # 展示配置项名称
        )
        return JsonResponse({'code': 1, 'data': list(rooms)})

    except Room.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '房间不存在'}, status=404)

    except Exception as e:
        print(traceback.format_exc())
        return JsonResponse({'code': 0, 'msg': '修改房间信息出现异常' + str(e)}, status=500)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsManager])
@transaction.atomic  # 添加事务管理
def delete_room(request, room_no):
    try:
        room = Room.objects.get(room_no=room_no)
        room.delete()
        return JsonResponse({'code': 1, 'msg': f'房间 {room_no} 已成功删除'})

    except Room.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': f'房间 {room_no} 不存在'})

    except Exception as e:
        import traceback
        print(traceback.format_exc())  # 打印堆栈跟踪，仅在开发环境中使用
        return JsonResponse({'code': 0, 'msg': '删除房间出现异常: ' + str(e)})


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsManager])  # 是否能访问看是否能通过所有权限
@transaction.atomic  # 添加事务管理
def get_customer(request):  # 显示全部信息
    try:
        obj_customer = Customer.objects.all().values()
        customers = list(obj_customer)
        return JsonResponse({'code': 1, 'data': customers}, safe=False)
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': '获取顾客信息出现异常:' + str(e)})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsManager])
@transaction.atomic  # 添加事务管理
def query_customer(request):
    # 使用 request.data 获取请求数据
    input_str = request.data.get('inputstr')  # 获取 'inputstr'

    if not input_str:
        return JsonResponse({'code': 0, 'msg': '请求缺少参数: inputstr'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        obj_customer = Customer.objects.filter(
            Q(name__icontains=input_str) | Q(room__room_no=input_str) | Q(checkOutTime__icontains=input_str) | Q(
                checkInTime__icontains=input_str) | Q(idCardNo__icontains=input_str) | Q(
                mobile__icontains=input_str) | Q(status__icontains=input_str))

        customers = [model_to_dict(customer) for customer in obj_customer]
        return JsonResponse({'code': 1, 'data': customers}, status=status.HTTP_200_OK)

    except Exception as e:
        import traceback
        print(traceback.format_exc())  # 打印堆栈跟踪
        return JsonResponse({'code': 0, 'msg': '查询顾客信息出现异常: ' + str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsManager])
@transaction.atomic  # 添加事务管理
def add_customer(request):
    try:
        data = request.data  # 使用 request.data 直接获取 JSON 数据
        # 确保所有必需的字段存在
        required_fields = ['name', 'roomNo', 'checkInTime', 'gender', 'idCardNo', 'mobile', 'balance',
                           'resideTimePeriod']
        for field in required_fields:
            if field not in data:
                return JsonResponse({'code': 0, 'msg': f'缺少必需字段: {field}'}, status=status.HTTP_400_BAD_REQUEST)

        # 获取房间对象
        room_no = data['roomNo']
        room = Room.objects.get(room_no=room_no)

        # 更新房间状态为已入住
        room.room_status = 'occupied'
        room.save()

        obj_customer = Customer(
            name=data['name'],
            room_id=data['roomNo'],  # 使用外键的ID来设置房间
            checkInTime=data['checkInTime'],
            gender=data['gender'],
            checkOutTime=data.get('checkOutTime', None),  # 允许为空
            idCardNo=data['idCardNo'],
            mobile=data['mobile'],
            image=data.get('image', None),  # 允许为空
            balance=data['balance'],
            resideTimePeriod=data['resideTimePeriod'],
            status=data.get('status', None)
        )
        obj_customer.cno = get_cno()
        obj_customer.save()

        obj_customers = Customer.objects.all().values()
        customers = list(obj_customers)
        return JsonResponse({'code': 1, 'data': customers})

    except Exception as e:
        print(traceback.format_exc())  # 打印堆栈跟踪
        return JsonResponse({'code': 0, 'msg': '添加顾客信息出现异常: ' + str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsManager])
@transaction.atomic  # 添加事务管理
def update_customer(request):
    try:
        data = request.data  # 使用 request.data 直接获取 JSON 数据
        customer_id = data.get('cno')

        if not customer_id:
            return JsonResponse({'code': 0, 'msg': '缺少顾客编号: cno'}, status=status.HTTP_400_BAD_REQUEST)

        obj_customer = Customer.objects.get(cno=customer_id)

        if data.get('status') == '已退宿':
            # 获取房间对象
            room_no = data['roomNo']
            room = Room.objects.get(room_no=room_no)

            # 更新房间状态为已入住
            room.room_status = 'vacant'
            room.save()

        obj_customer.name = data.get('name', obj_customer.name)
        obj_customer.checkInTime = data.get('checkInTime', obj_customer.checkInTime)
        obj_customer.gender = data.get('gender', obj_customer.gender)
        obj_customer.checkOutTime = data.get('checkOutTime', obj_customer.checkOutTime)
        obj_customer.idCardNo = data.get('idCardNo', obj_customer.idCardNo)
        obj_customer.mobile = data.get('mobile', obj_customer.mobile)
        obj_customer.status = data.get('status', obj_customer.status)

        # 处理并更新图像
        if data.get('image'):
            if obj_customer.image:  # 如果之前有图片，先删除旧图
                photo_path = path.join(settings.MEDIA_ROOT, str(obj_customer.image))
                if path.isfile(photo_path):  # 检查文件是否存在
                    remove(photo_path)  # 删除文件
            obj_customer.image = data['image']  # 更新为新图片

        obj_customer.balance = data.get('balance', obj_customer.balance)
        obj_customer.resideTimePeriod = data.get('resideTimePeriod', obj_customer.resideTimePeriod)

        # 保存更新
        obj_customer.save()

        obj_customers = Customer.objects.all().values()
        customers = list(obj_customers)
        return JsonResponse({'code': 1, 'data': customers})

    except Exception as e:
        print(traceback.format_exc())  # 打印堆栈跟踪
        return JsonResponse({'code': 0, 'msg': '修改顾客信息出现异常: ' + str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsManager])
@transaction.atomic  # 添加事务管理
def delete_customer(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        obj_customer = Customer.objects.get(cno=str(data))
        if obj_customer.image:
            photo_path = path.join(settings.MEDIA_ROOT, str(obj_customer.image))
            if path.isfile(photo_path):  # 检查文件是否存在
                remove(photo_path)  # 删除文件
        obj_customer.delete()
        obj_customers = Customer.objects.all().values()
        customers = list(obj_customers)
        return JsonResponse({'code': 1, 'data': customers})

    except Exception as e:
        import traceback
        print(traceback.format_exc())  # 打印堆栈跟踪
        return JsonResponse({'code': 0, 'msg': '删除时出现异常:' + str(e)})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsManager])
@transaction.atomic  # 添加事务管理
def delete_customers(request):
    # 接受删除的顾客信息
    data = json.loads(request.body.decode('utf-8'))
    try:
        for one_customer in data['customers']:
            obj_customer = Customer.objects.get(cno=str(one_customer['cno']))
            if obj_customer.image:
                photo_path = path.join(settings.MEDIA_ROOT, str(obj_customer.image))
                if path.isfile(photo_path):  # 检查文件是否存在
                    remove(photo_path)  # 删除文件
            obj_customer.delete()
        obj_customer = Customer.objects.all().values()
        # 把结果转为list
        customers = list(obj_customer)
        return JsonResponse({'code': 1, 'data': customers})

    except Exception as e:
        # 如果出现异常，返回
        import traceback
        print(traceback.format_exc())  # 打印堆栈跟踪
        return JsonResponse({'code': 0, 'msg': '批量删除时出现异常:' + str(e)})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@transaction.atomic  # 添加事务管理
def upload(request):
    rev_file = request.FILES.get('avatar')
    if not rev_file:
        return JsonResponse({'code': 0, 'msg': '未检测到图片文件'}, status=400)
    new_name = get_random_str()
    file_extension = path.splitext(rev_file.name)[1]
    file_path = path.join(settings.MEDIA_ROOT, new_name + file_extension)
    # 写入
    try:
        f = open(file_path, 'wb')
        for chunk in rev_file.chunks():
            f.write(chunk)
        f.close()
        return JsonResponse({'code': 1, 'name': new_name + file_extension})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': '上传文件出现异常:' + str(e)})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@transaction.atomic  # 添加事务管理
def customer_reserve(request):
    try:
        data = request.data

        required_fields = ['name', 'roomNo', 'gender', 'idCardNo', 'mobile', 'balance', 'resideTimePeriod',
                           'checkInTime']
        for field in required_fields:
            if field not in data:
                return JsonResponse({'code': 0, 'msg': f'缺少必需字段: {field}'}, status=status.HTTP_400_BAD_REQUEST)

        room_no = data['roomNo']
        room = Room.objects.get(room_no=room_no)

        room.room_status = 'reserved'
        room.save()

        obj_customer = Customer(
            name=data['name'],
            room_id=data['roomNo'],  # 使用外键的ID来设置房间
            gender=data['gender'],
            idCardNo=data['idCardNo'],
            mobile=data['mobile'],
            image=data.get('image', None),  # 允许为空
            balance=data['balance'],
            resideTimePeriod=data['resideTimePeriod'],
            status='已预订',
            checkInTime=data['checkInTime'],
        )
        obj_customer.cno = get_cno()
        obj_customer.save()

        return JsonResponse({'code': 1})

    except Exception as e:
        print(traceback.format_exc())  # 打印堆栈跟踪
        return JsonResponse({'code': 0, 'msg': '添加顾客信息出现异常: ' + str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@transaction.atomic  # 添加事务管理
def customer_cancel_reserve(request):
    try:
        data = request.data

        if 'cno' not in data:
            return JsonResponse({'code': 0, 'msg': '缺少必需字段: cno'}, status=status.HTTP_400_BAD_REQUEST)

        if 'roomNo' not in data:
            return JsonResponse({'code': 0, 'msg': '缺少必需字段: roomNo'}, status=status.HTTP_400_BAD_REQUEST)

        cno = data['cno']
        customer = Customer.objects.get(cno=str(cno))
        customer.status = '已取消预订'
        customer.save()

        room_no = data['roomNo']
        room = Room.objects.get(room_no=room_no)

        room.room_status = 'vacant'
        room.save()

        return JsonResponse({'code': 1})

    except Exception as e:
        print(traceback.format_exc())  # 打印堆栈跟踪
        return JsonResponse({'code': 0, 'msg': '取消预订出现异常: ' + str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_customer_reservations(request, user_id):
    try:
        # 权限检查：普通用户只能查看自己的记录
        if not request.user.is_staff and request.user.id != int(user_id):
            return JsonResponse(
                {'code': 0, 'msg': '无权查看该用户记录'},
                status=status.HTTP_403_FORBIDDEN
            )

        # 直接查询并返回结果
        reservations = Customer.objects.filter(user_id=user_id) \
            .select_related('room') \
            .order_by('-checkInTime')

        # 转换为字典列表
        reservations_data = []
        for r in reservations:
            reservations_data.append({
                'cno': r.cno,
                'name': r.name,
                'room_no': r.room.room_no if r.room else None,
                'check_in_time': r.checkInTime,
                'check_out_time': r.checkOutTime,
                'resideTimePeriod': r.resideTimePeriod,
                'status': r.status
            })

        return JsonResponse({
            'code': 1,
            'data': reservations_data
        })

    except ObjectDoesNotExist:
        return JsonResponse(
            {'code': 0, 'msg': '用户不存在'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return JsonResponse(
            {'code': 0, 'msg': f'获取租住记录失败: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
