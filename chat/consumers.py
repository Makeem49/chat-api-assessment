import json

from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from channels.exceptions import DenyConnection

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print(self.scope, 'scope')
        headers = self.scope.get('headers')
        
        headers = dict(headers)
        print(headers)
        # print(self.scope, 'scope')
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        
        print(self.channel_name)
        
        if self.room_name.capitalize() != 'Lobby':
           await self.close()
        

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()
        

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    # async def receive(self, text_data):
    #     # text_data_json = json.loads(text_data)
    #     # message = text_data_json["message"]

    #     # Send message to room group
    #     await self.channel_layer.group_send(
    #         self.room_group_name, {"type": "chat_message", "message": text_data}
    #     )
        
    async def receive_json(self, content, **kwargs):
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": content}
        )
        return await super().receive_json(content, **kwargs)

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))