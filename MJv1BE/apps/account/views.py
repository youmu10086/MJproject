# apps/account/views.py
import json

from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

import traceback
from apartment.permissions import IsManager, IsAdmin
from django.forms.models import model_to_dict

CustomUser = get_user_model()


def set_refresh_cookie(response, refresh):
    response.set_cookie(
        key='refreshToken',
        value=str(refresh),
        httponly=True,
        secure=False,  # 生产环境中请将此设置为 True
        samesite='Lax',
        max_age=30 * 24 * 60 * 60,
    )


# apps/account/views.py 新增密码重置视图
@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        username = data['username']
        new_password = data['password']

        # 验证用户是否存在且邮箱匹配
        user = CustomUser.objects.get(username=username)

        # 使用 Django 的密码哈希机制
        user.set_password(new_password)
        user.save()

        return Response({'code': 1, 'msg': '密码重置成功'}, status=status.HTTP_200_OK)

    except CustomUser.DoesNotExist:
        return Response({'code': 0, 'msg': '用户不存在或邮箱不匹配'},
                        status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'code': 0, 'msg': f'重置密码失败: {str(e)}'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def enroll(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        # role = data.get('role', 'customer')  # role不存在默认为customer
        # if role not in [choice[0] for choice in CustomUser.ROLE_CHOICES]:   # 检查用户提交的角色是否在预定义的有效角色列表中，如果用户提交的 role 不在合法列表中（如用户试图设置为 'hacker'），则强制将 role 重置为 'customer'。
        role = 'customer'  # 默认为顾客

        obj_user = CustomUser.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        obj_user.role = 'customer'
        obj_user.save()  # 保存角色信息
        refresh = RefreshToken.for_user(obj_user)
        access = str(refresh.access_token)

        response = Response({
            'access': access,
            'username': obj_user.username,
            'role': role,
            'id': obj_user.id,
        }, status=status.HTTP_201_CREATED)

        set_refresh_cookie(response, refresh)
        return response
    except Exception as e:
        return Response({'code': 0, 'msg': '注册时出现异常:' + str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def add_employee(request):
    data = json.loads(request.body.decode('utf-8'))  # 解析请求数据
    try:
        # 从请求中提取角色、用户名、电子邮件、电话和密码
        role = data.get('role', 'manager')  # 默认为 manager
        username = data['name']  # 使用姓名作为用户名
        email = data['email']
        password = data['password']

        obj_user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        obj_user.role = role
        obj_user.save()  # 保存用户信息

        response = Response({
            'username': obj_user.username,
            'role': role
        }, status=status.HTTP_201_CREATED)

        return response
    except Exception as e:
        return Response({'code': 0, 'msg': '注册时出现异常:' + str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)
    try:
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)
            role = user.role
            user_id = user.id
            response = Response({'access': access, 'username': username, 'role': role, 'id': user_id}, status=status.HTTP_200_OK)
            set_refresh_cookie(response, refresh)
            return response
        else:
            return Response({'msg': '用户名或密码错误'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'code': 0, 'msg': '登录时出现异常:' + str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def logout(request):
    try:
        # 清除 Cookie
        response = Response({'message': '登出成功'}, status=status.HTTP_200_OK)
        response.delete_cookie('refreshToken')

        return response
    except Exception as e:
        return Response({'code': 0, 'msg': '登出时出现异常:' + str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # 确保用户已认证
def get_userRole(request):
    user = request.user  # 从请求中获取已认证的用户
    try:
        if user is not None:
            role = user.role
            response = Response({'role': role}, status=status.HTTP_200_OK)
            return response
        else:
            return Response({'msg': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'code': 0, 'msg': '登录时出现异常:' + str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    refreshToken = request.COOKIES.get('refreshToken')
    if not refreshToken:
        return Response({'msg': '访问过期，请重新登录'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        refresh = RefreshToken(refreshToken)
        user = CustomUser.objects.get(id=refresh['user_id'])

        # 生成新的 Token
        new_refresh = RefreshToken.for_user(user)
        new_access = str(new_refresh.access_token)

        response = Response({
            'access': new_access,
            'username': user.username,
            'role': user.role
        }, status=status.HTTP_200_OK)

        # 更新 refreshToken cookie
        set_refresh_cookie(response, new_refresh)
        return response
    except Exception as e:
        return Response({'msg': f'Token refresh failed: {str(e)}'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin])  # 是否能访问看是否能通过所有权限
def get_user(request):  # 显示全部信息
    try:
        obj_user = CustomUser.objects.all().values()
        users = list(obj_user)
        return JsonResponse({'code': 1, 'data': users}, safe=False)
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': '获取用户信息出现异常:' + str(e)})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsAdmin])
def query_user(request):  # 查询功能
    data = json.loads(request.body.decode('utf-8'))
    try:
        obj_user = (
            CustomUser.objects.filter(Q(name__icontains=data['inputstr'])))
        users = [model_to_dict(user) for user in obj_user]
        return JsonResponse({'code': 1, 'data': users})
    except Exception as e:
        print(traceback.format_exc())  # 打印堆栈跟踪
        return JsonResponse({'code': 0, 'msg': '查询用户信息时出现异常:' + str(e)})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsAdmin])
def update_user(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        obj_user = CustomUser.objects.get(id=data['id'])
        obj_user.username = data['username']
        # obj_user.mobile = data['mobile']
        obj_user.save()
        obj_user = CustomUser.objects.all().values()
        users = list(obj_user)
        return JsonResponse({'code': 1, 'data': users})
    except Exception as e:
        print(traceback.format_exc())  # 打印堆栈跟踪
        return JsonResponse({'code': 0, 'msg': '修改用户信息出现异常:' + str(e)})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsAdmin])
def delete_user(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        obj_user = CustomUser.objects.get(id=str(data))
        obj_user.delete()
        obj_users = CustomUser.objects.all().values()
        users = list(obj_users)
        return JsonResponse({'code': 1, 'data': users})

    except Exception as e:
        print(traceback.format_exc())  # 打印堆栈跟踪
        return JsonResponse({'code': 0, 'msg': '删除时出现异常:' + str(e)})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsAdmin])
def delete_users(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        for one_user in data['users']:
            obj_customer = CustomUser.objects.get(id=str(one_user['id']))
            obj_customer.delete()
        obj_customers = CustomUser.objects.all().values()
        customers = list(obj_customers)
        return JsonResponse({'code': 1, 'data': customers})

    except Exception as e:
        print(traceback.format_exc())  # 打印堆栈跟踪
        return JsonResponse({'code': 0, 'msg': '批量删除时出现异常:' + str(e)})
