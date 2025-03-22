import json
from os import path, remove

from django.conf import settings
from django.db.models import Q  # 导入q查询
from django.forms.models import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models.customer import *
from .models.room import *
from .myTool import *
from .permissions import IsManager


# Create your views here.
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
        obj_room = Room.objects.all().values()
        rooms = list(obj_room)
        return JsonResponse({'code': 1, 'data': rooms}, safe=False)
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': '获取房间信息时出现异常:' + str(e)})


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
        obj_customer = Customer.objects.all().values()
        customers = list(obj_customer)
        return JsonResponse({'code': 1, 'data': customers})
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
