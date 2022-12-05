import time
import jwt
from rest_framework import status
from rest_framework.response import Response
from config.jwt import JWT_HEADERS, SALT, TOKEN_EXPRIED


def get_token_from_request(request):
    return request.data.get("token") or request.GET.get("token") or request.META.get("HTTP_TOKEN")


def require_login(func):
    def inner(self, request, *args, **kwargs):
        token = get_token_from_request(request)
        if not check_token(token):
            return Response({"detail": "未登录"}, status=status.HTTP_401_UNAUTHORIZED)
        return func(self, request, *args, **kwargs)

    return inner


def gene_token(username):
    exp = int(time.time() + TOKEN_EXPRIED)
    payload = {
        "username": username,
        "exp": exp
    }
    token = jwt.encode(payload=payload, key=SALT, algorithm='HS256', headers=JWT_HEADERS).decode('utf-8')
    return token


def check_token(token):
    try:
        res = jwt.decode(token, SALT, True, algorithm='HS256')
        return res
    except:
        return False
