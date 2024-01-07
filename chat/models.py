from django.db import models
from user.models import User 
import uuid
# Create your models here.



class Room(models.Model):
    name = models.CharField(max_length=150)
    users = models.ManyToManyField(User, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def get_online_count(self):
        """
        Description: Get the total number of users in the room 
        :preturn self: Number
        """
        return self.users.count()

    def join(self, user):
        """
        Description: Adding user to the room conversation 
        :param user: Id 
        :return None:
        """
        self.users.add(user)
        self.save()

    def leave(self, user):
        """
        Description: Removing user from the room conversation 
        
        :param user: Id 
        :return None:
        """
        self.users.remove(user)
        self.save()

    def __str__(self):
        return f"{self.name} ({self.get_online_count()})"
    
    
class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages_from_me")
    to_users = models.ManyToManyField(User, null=True, related_name="messages_to_users", through='UserMessage')
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)
    # read = models.BooleanField(default=False)
    # read_timestamp = models.DateTimeField(null=True)
    
    def __str__(self):
        return f"From {self.from_user.username} to {self.room.name} {self.content} [{self.timestamp}]"
    
    
class UserMessage(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.DateField(default=False)


    