import jwt
from urllib.parse import parse_qs
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.conf import settings

User = get_user_model()

@database_sync_to_async
def get_user_from_access_token(scope):
    """Function use to decode a access_token to retreive the user
    :param access_token: str
    :return user: Instance of User or None
    
    """
    try:
        
        access_token = scope.get('token', None)
        if not access_token: 
            return None 
        
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
        user = User.objects.get(id=payload['user_id'])
       
        if user is None:
            return None 
        return user

    except Exception as e:
        # Handle exceptions (e.g., TokenError)
        print(f"Error decoding access token: {e}")
        return None
    

class TokenAuthenticationMiddleware:
    """
    Simple jwt base token authorization
    
    Client connecting to the websocket should pass thier token to the query string parameter
    
    Example:
        ?url: ws://127.0.0.1:8000/ws/chat/lobby/?token=uyuy89er98u39.4098080982yrhjkkjdf.jiouoyyw
    """
    
    def __init__(self, app) -> None:
        self.app = app 
        
    async def __call__(self, scope, receive, send):
        """
        
        """
        query_params = parse_qs(scope["query_string"].decode())
        
        token = query_params.get('token', None)
        
        if token is None:
            return await self.app(scope, receive, send) 
        else:
            token = query_params["token"][0]
            scope["token"] = token
            scope["user"] = await get_user_from_access_token(scope)
        
        return await self.app(scope, receive, send)
    
    