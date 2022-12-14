import io

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from pkg.auth import require_login, gene_token
from pkg import code, enctypt
from .models import User, Level
from .serializers import UserSerializer
import base64


class UserLoginView(APIView):

    def get(self, request):
        img, code_str = code.gene_code()
        buffered = io.BytesIO()
        img.save(buffered, format='PNG')
        img_str = base64.b64encode(buffered.getvalue())
        md5_str = enctypt.md5(img_str, 1)
        code.cache_code(md5_str, code_str)
        return Response({"img": img_str}, status=status.HTTP_200_OK)

    def post(self, request):
        username = request.data.get('username')
        pwd = request.data.get('password')
        img_str = request.data.get('img')
        code_str = request.data.get('code')
        if not code_str or not img_str:
            return Response({"detail": "请输入验证码"}, status=status.HTTP_401_UNAUTHORIZED)
        md5_str = enctypt.md5(img_str, 2)
        res = bool(code.check_code(md5_str, str(code_str).upper()))
        if not res:
            return Response({"detail": "验证码错误"}, status=status.HTTP_400_BAD_REQUEST)
        if not User.objects.filter(username=username):
            return Response({"detail": "账号或密码错误"}, status=status.HTTP_401_UNAUTHORIZED)
        user = User.objects.get(username=username)
        if user.check_password(pwd):
            token = gene_token(user.username)
            return Response({"detail": "登录成功", "token": token})
        return Response({"detail": "账号或密码错误"}, status=status.HTTP_401_UNAUTHORIZED)


class UserCreateView(APIView):
    @require_login
    def get(self, request):
        return Response(UserSerializer(User.objects.all(), many=True).data, status=status.HTTP_200_OK)

    @require_login
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        level = request.data.get('level') or 1
        _level = Level.objects.get(id=level)
        if not username or not password:
            return Response({"detail": "请输入用户名和密码"}, status=status.HTTP_400_BAD_REQUEST)
        User.objects.create_user(
            username=username,
            password=password,
            level=_level
        )
        return Response({"detail": "success"}, status=status.HTTP_200_OK)
