# apps/account/views.py
import json

from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def enroll(request):
#     data = json.loads(request.body.decode('utf-8'))
#
#     try:
#         obj_user = User.objects.create_user(username=data['username'], email=data['email'], password=data['password'])
#
#         # 生成 Access 和 Refresh Token
#         refresh = RefreshToken.for_user(obj_user)
#         access = str(refresh.access_token)
#
#         # 使用 JSON 响应返回 Access Token
#         response = Response({'access': access, 'username': obj_user.username}, status=status.HTTP_201_CREATED)
#
#         response.set_cookie(
#             key='refreshToken',
#             value=str(refresh),
#             httponly=True,
#             secure=False,  # 本地测试可以设置为 False，生产环境下改为 True
#             samesite='Lax',
#             max_age=7 * 24 * 60 * 60,
#         )
#         return response
#     except Exception as e:
#         return Response({'code': 0, 'msg': '注册时出现异常:' + str(e)}, status=status.HTTP_400_BAD_REQUEST)

CustomUser = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def enroll(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        role = data.get('role', 'customer')  # role不存在默认为customer
        if role not in [choice[0] for choice in CustomUser.ROLE_CHOICES]:   # 检查用户提交的角色是否在预定义的有效角色列表中，如果用户提交的 role 不在合法列表中（如用户试图设置为 'hacker'），则强制将 role 重置为 'customer'。
            role = 'customer'  # 默认为顾客

        obj_user = CustomUser.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        obj_user.role = role
        obj_user.save()  # 保存角色信息
        refresh = RefreshToken.for_user(obj_user)
        access = str(refresh.access_token)
        response = Response({'access': access, 'username': obj_user.username, 'role': role}, status=status.HTTP_201_CREATED)
        response.set_cookie(
            key='refreshToken',
            value=str(refresh),
            httponly=True,
            secure=False,  # 本地测试可以设置为 False，生产环境下改为 True
            samesite='Lax',
            max_age=7 * 24 * 60 * 60,
        )
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
            response = Response({'access': access, 'username': username, 'role': role}, status=status.HTTP_200_OK)
            response.set_cookie(
                key='refreshToken',
                value=str(refresh),
                httponly=True,
                secure=False,
                samesite='Lax',
                max_age=7 * 24 * 60 * 60,
            )
            return response
        else:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'code': 0, 'msg': '登录时出现异常:' + str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def logout(request):
    # 清除 Cookie
    response = Response({'message': '登出成功'}, status=status.HTTP_200_OK)
    response.delete_cookie('refreshToken')  # 假设你的 Cookie 名称是 'refreshToken'

    return response


@api_view(['POST'])
def refresh_token(request):
    refreshToken = request.COOKIES.get('refreshToken')

    if not refresh_token:
        return Response({'error': 'No refresh token provided.'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        # 验证 Refresh Token
        token = RefreshToken(refreshToken)
        access = str(token.access_token)
        return Response({'access': access}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
