from rest_framework import serializers
from chat.models import Message
from user.serializers import UserSerializer


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
            "timestamp",
            "read",
        )

    def get_room(self, obj):
        return str(obj.room.id)

    def get_from_user(self, obj):
        return UserSerializer(obj.from_user).data

    def get_to_user(self, obj):
        return UserSerializer(obj.to_users, many=True).data