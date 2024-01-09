from datetime import datetime
import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from chat.models import Room, Message
from asgiref.sync import async_to_sync, sync_to_async
from chat.serializers import MessageSerializer
from chat.utils import (
                        read_message,
                        users_in_room,
                        create_message, 
                        get_message_data,
                        add_user_to_room, 
                        get_all_messages, 
                        get_messages_data, 
                        get_or_create_room, 
                        get_all_user_in_a_room, 
                        get_total_messages_number, 
                        remove_user_from_room,
                        UUIDEncoder
                        )




class ChatConsumer(AsyncJsonWebsocketConsumer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.user = None
        self.room = None 
        self.room_group_name = None 
    
    async def connect(self):
        self.user = self.scope.get("user")
        print(self.user, 'user')
        
        if not self.user:
            await self.close(code=403)
        else:
            await self.accept()

            self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
            self.room_group_name = f"chat_{self.room_name}"
            
            self.room, created =  await get_or_create_room(self.room_name)
            await add_user_to_room(self.room, self.user.id)
            
            # Join room group
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            
            users = await users_in_room(self.room) # get the number of users in the room chat 
            
            
            # Notifying room of users in the room 
            await self.send_json(
                {
                    "type" : "online_user_list",
                    "users" : [user for user in users]
                }
            )
            
            # Notifying room of new user        
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "user_join",
                    "user": f"{self.user.username if self.user.username else self.user.first_name} joined the chat"
                },
            )
            
            
            messages = await get_all_messages(self.room, 20)
            message_count = await get_total_messages_number(self.room)
            message_data = await get_messages_data(messages)
            
            await self.send_json(
                {
                    "type" : "last_20_messages",
                    "messages" : message_data,
                    "has_more" : message_count > 10
                }
            )
               
        
    async def disconnect(self, close_code):
                user = self.user
                if user:
                    # Notify other users about the user leaving
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            "type": "user_leave",
                            "user": user.username if user.username else user.first_name,
                            "message" : "User left"
                        }
                    )

                    await remove_user_from_room(self.room, self.user)
                    await self.channel_layer.group_discard(self.room_name, self.channel_name)
                    
                    return super().disconnect(close_code)
                else:
                    return super().disconnect(400)
        
        
    async def receive_json(self, content, **kwargs):
        message_type = content.get('type')
        
        if message_type.lower() == 'chat_message':
            content = content.get('content')
            recievers = await self.get_recievers(self.room.id, self.user)

            messsage =  await create_message(self.user, recievers, self.room, content)
                
            message_data = await get_message_data(messsage)
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat_message", "message": message_data}
            )
            return await super().receive_json(content, **kwargs)
        
        else:
            await self.send_json({
                "status" : "No event specify",
                "status" : 400
            })
            
            self.disconnect(400)

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
        
    async def user_join(self, event):
        users = event['user']
        await self.send_json({"user": users})
          
    async def user_leave(self, event):
        await self.send_json(event)   
    
    async def get_recievers(self, id, sender):
        return await get_all_user_in_a_room(id, sender)
    
    @classmethod
    async def encode_json(cls, content):
        return json.dumps(content, cls=UUIDEncoder)
    
    async def notification(self, event):
        await self.send(text_data=json.dumps({"message": event["message"]}))
        
        


class ReadChatConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.user = None
        self.room = None 
        self.room_group_name = None 
    
    async def connect(self):
        self.user = self.scope.get("user")
        print(self.user, 'user')
        
        if not self.user:
            await self.close(code=403)
        else:  
            await self.accept()
            
            self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
            self.room_group_name = f"chat_{self.room_name}"
            
            self.room, created =  await get_or_create_room(self.room_name)
            
            await self.send_json(
                {
                    "type" : "online_user_list",
                    "users" : "User"
                }
            )

        
    async def disconnect(self, close_code):
            return super().disconnect(close_code)
        
        
    async def receive_json(self, content, **kwargs):
        message_type = content.get('type')
        
        if message_type == "read_messages":
            message_id = content.get('message_id') # update 
            to_user = self.user
            await read_message(self.room, message_id, to_user)
            
            await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "notification",
                        "message": f"{self.user.username} read the message with id {message_id}",
                    },
                )
            
            
        else:
            await self.send_json({
                "status" : "No event specify",
                "status" : 400
            })
            
            self.disconnect(400)
            
    async def notification(self, event):
        await self.send(text_data=json.dumps({"message": event["message"]}))
        

    