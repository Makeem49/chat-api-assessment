from datetime import datetime
import json
from uuid import UUID
from channels.db import database_sync_to_async
from chat.models import Room, Message
from chat.serializers import MessageSerializer
from user.models import User

@database_sync_to_async
def get_or_create_room(name):
    obj, created =  Room.objects.get_or_create(name=name)
    return [obj, created]


@database_sync_to_async
def users_in_room(room):
    return [user.id for user in room.users.all()]


@database_sync_to_async
def add_user_to_room(room, id):
    room.users.add(id)
    
@database_sync_to_async
def get_all_messages(room, num_of_message=50):
    return room.messages.all().order_by("-timestamp")[0:num_of_message]

@database_sync_to_async
def get_total_messages_number(room):
    return room.messages.all().count()

@database_sync_to_async
def get_messages_data(messages):
    data = MessageSerializer(messages, many=True).data
    return data 


@database_sync_to_async
def get_message_data(messages):
    data = MessageSerializer(messages).data
    return data 


@database_sync_to_async
def remove_user_from_room(room, user):
    room.users.remove(user.id)
    
    
@database_sync_to_async
def get_user(id):
    return User.obj.filter(id=id)

@database_sync_to_async
def get_all_user_in_a_room(id):
    room = Room.objects.filter(id=id).first()
    users = room.users.all()
    return users 


@database_sync_to_async
def create_message(sender, receivers, room, content):
    message = Message.objects.create(
        room=room, 
        from_user = sender,
        content=content
    )
    message.to_users.set(receivers, through_defaults={"read":False})
    return message

@database_sync_to_async
def read_message(room, message_id, to_user):
        messages_to_me = room.messages.filter(to_users=to_user, id=message_id)
        messages_to_me.update(read=True, read_timestamp=datetime.now())


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)
    
    
