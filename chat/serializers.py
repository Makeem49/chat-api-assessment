from rest_framework import serializers
from chat.models import Message, UserMessage
from user.serializers import UserSerializer


class RecieverSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = UserMessage
        fields = [
            'read',
            'date_read',
            'user'
        ]


    def get_user(self, obj):
        user = UserSerializer(obj.user).data
        return user 

class MessageSerializer(serializers.ModelSerializer):
    from_user = serializers.SerializerMethodField()
    to_user = serializers.SerializerMethodField()
    room = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = (
            "id",
            'room',
            "room",
            "from_user",
            "to_user",
            "content",
            "date_created",
            # "read",
        )

    def get_room(self, obj):
        return str(obj.room.id)

    def get_from_user(self, obj):
        return UserSerializer(obj.from_user).data

    def get_to_user(self, obj):
        user_message = UserMessage.objects.filter(user__in=obj.to_users.all()).all()
        return RecieverSerializer(user_message, many=True).data