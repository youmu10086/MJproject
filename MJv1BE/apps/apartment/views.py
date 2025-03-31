import traceback
from os import path, remove

from django.conf import settings
from django.db import transaction
from django.db.models import Q, F  # 导入q查询
from django.forms.models import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.utils import json
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Customer, Room, RoomConfig
from .myTool import *
from .permissions import IsManager


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsManager])  # 是否能访问看是否能通过所有权限
def get_customer(request):  # 显示全部信息
    try:
        obj_customer = Customer.objects.all().values()
        customers = list(obj_customer)
        return JsonResponse({'code': 1, 'data': customers}, safe=False)
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': '获取顾客信息出现异常:' + str(e)})


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


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsManager])
def query_customer(request):  # 查询功能
    data = json.loads(request.body.decode('utf-8'))
    try:
        obj_customer = (
            Customer.objects.filter(Q(name__icontains=data['inputstr']) | Q(roomNo=data['inputstr']) |
                                    Q(checkOutTime__icontains=data['inputstr']) | Q(
                checkInTime__icontains=data['inputstr'])
                                    | Q(idCardNo__icontains=data['inputstr']) | Q(mobile__icontains=data['inputstr'])))
        customers = [model_to_dict(customer) for customer in obj_customer]
        return JsonResponse({'code': 1, 'data': customers})
    except Exception as e:
        import traceback
        print(traceback.format_exc())  # 打印堆栈跟踪
        return JsonResponse({'code': 0, 'msg': '查询顾客信息出现异常:' + str(e)})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsManager])
def add_customer(request):  # 添加功能
    # 接受添加的顾客信息
    data = json.loads(request.body.decode('utf-8'))
    try:
        obj_customer = Customer(name=data['name'], roomNo=data['roomNo'], checkInTime=data['checkInTime'],
                                gender=data['gender'], checkOutTime=data['checkOutTime'], idCardNo=data['idCardNo'],
                                mobile=data['mobile'], image=data['image'], balance=data['balance'],
                                resideTimePeriod=data['resideTimePeriod'])
        obj_customer.cno = get_cno()
        obj_customer.save()
        customers = Customer.objects.all().values()
        customers_list = list(customers)
        return JsonResponse({'code': 1, 'data': customers_list})
    except Exception as e:
        import traceback
        print(traceback.format_exc())  # 打印堆栈跟踪
        return JsonResponse({'code': 0, 'msg': '添加顾客信息出现异常:' + str(e)})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsManager])
def update_customer(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        obj_customer = Customer.objects.get(cno=data['cno'])
        obj_customer.name = data['name']
        obj_customer.roomNo = data['roomNo']
        obj_customer.checkInTime = data['checkInTime']
        obj_customer.gender = data['gender']
        obj_customer.checkOutTime = data['checkOutTime']
        obj_customer.idCardNo = data['idCardNo']
        obj_customer.mobile = data['mobile']
        if obj_customer.image:
            photo_path = path.join(settings.MEDIA_ROOT, str(obj_customer.image))
            if path.isfile(photo_path):  # 检查文件是否存在
                remove(photo_path)  # 删除文件
        obj_customer.image = data['image']
        obj_customer.balance = data['balance']
        obj_customer.resideTimePeriod = data['resideTimePeriod']
        obj_customer.save()
        obj_customer = Customer.objects.all().values()
        customers = list(obj_customer)
        return JsonResponse({'code': 1, 'data': customers})
    except Exception as e:
        import traceback
        print(traceback.format_exc())  # 打印堆栈跟踪
        return JsonResponse({'code': 0, 'msg': '修改顾客信息出现异常:' + str(e)})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsManager])
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
def upload(request):
    """接受上传的文件"""
    rev_file = request.FILES.get('avatar')
    if not rev_file:
        return JsonResponse({'code': 0, 'msg': '未检测到图片文件'}, status=400)
    new_name = get_random_str()
    file_extension = path.splitext(rev_file.name)[1]  # 获取文件扩展名(.jpg)
    # settings.MEDIA_ROOT：这是Django配置文件中定义的一个设置，表示保存上传文件的目录的绝对路径。
    # new_name + file_extension：这是将之前生成的唯一文件名（new_name）与文件扩展名（file_extension）连接，形成完整的文件名（例如"unique_name.jpg"）。
    # os.path.join(...)：使用os.path.join()函数来构建一个完整的文件路径。这个函数会根据当前操作系统的文件路径分隔符（如Windows下为 \，Linux / Unix下为 /）正确地连接目录和文件名，从而生成完整的路径。
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
