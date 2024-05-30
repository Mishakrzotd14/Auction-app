from urllib.parse import parse_qs

from django.core.exceptions import ObjectDoesNotExist
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser

from rest_framework.authtoken.models import Token


@database_sync_to_async
def get_user_from_token(query):
    if b'token' in query:
        token_key = query[b'token'][0].decode()
        try:
            token = Token.objects.get(key=token_key)
            return token.user
        except ObjectDoesNotExist:
            return AnonymousUser()
    return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        token_name, token_key = scope['query_string'].decode().split('=')
        if token_name == 'token':
            scope['user'] = await get_user_from_token(token_key)
        return await super().__call__(scope, receive, send)


def TokenAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(AuthMiddlewareStack(inner))