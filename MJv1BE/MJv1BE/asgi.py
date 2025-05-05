from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat import routing  # 导入你的应用路由

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        routing.websocket_urlpatterns
    ),
})