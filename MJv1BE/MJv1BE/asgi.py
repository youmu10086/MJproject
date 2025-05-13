# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from django.urls import path
# from chat.consumers import TestConsumer
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MJv1BE.settings')
#
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter([
#             path('ws/test/', TestConsumer.as_asgi()),  # WebSocket 路由
#         ])
#     ),
# })