from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Room
from .serializers import RoomSerializer


# Create your views here.
class RoomView(APIView):
    def get(self, request):
        rid = request.GET.get('rid')
        if not rid:
            return Response({"detail": "未获取到房间编号"}, status=status.HTTP_400_BAD_REQUEST)
        _room = Room.objects.get(id=rid)
        if not _room:
            return Response({"detail": "房间信息异常"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(RoomSerializer(_room, many=True).data)

    def post(self, request):
        room_id = request.data.get('room_id')
        space = request.data.get('space') or 1
        is_hotwater = request.data.get('space') or 0
        is_computer = request.data.get('space') or 0
        is_used = request.data.get('space') or 0
        value = request.data.get('value')
        if not room_id or not value:
            return Response({"detail": "房间信息不完整"}, status=status.HTTP_400_BAD_REQUEST)
        if Room.objects.filter(room_id=room_id):
            return Response({"detail": "房间已存在"}, status=status.HTTP_400_BAD_REQUEST)
        Room.objects.create(
            room_id=room_id,
            space=space,
            is_hotwater=is_hotwater,
            is_computer=is_computer,
            is_used=is_used,
            value=value
        )
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)

    def delete(self, request):
        rid = request.DELETE.get('rid')
        if not rid:
            return Response({"detail": "未获取到房间号"}, status=status.HTTP_400_BAD_REQUEST)
        _room = Room.objects.get(id=rid)
        if not _room:
            return Response({"detail": "房间信息异常"}, status=status.HTTP_400_BAD_REQUEST)
        _room.delete()
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)


class RoomViews(APIView):
    def get(self, request):
        return Response(RoomSerializer(Room.objects.all(), many=True).data)

    def post(self, request):
        pass

    def delete(self, request):
        pass
