import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 接受 WebSocket 连接
        await self.accept()
        await self.send(text_data=json.dumps({
            'message': 'WebSocket connection established!',
        }))

    async def disconnect(self, close_code):
        # 处理 WebSocket 断开
        print('WebSocket disconnected')

    async def receive(self, text_data=None, bytes_data=None):
        # 处理接收到的消息
        if text_data:
            data = json.loads(text_data)
            message = data.get('message', '')
            await self.send(text_data=json.dumps({
                'message': f'Echo: {message}',
            }))