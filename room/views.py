from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Room, Floor, FreeRoom
from .serializers import RoomSerializer


# Create your views here.
class RoomView(APIView):
    def get(self, request):
        """获取指定房间信息"""
        rid = request.GET.get('rid')
        if not rid:
            return Response({"detail": "未获取到房间编号"}, status=status.HTTP_400_BAD_REQUEST)
        _room = Room.objects.get(id=rid)
        if not _room:
            return Response({"detail": "房间信息异常"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(RoomSerializer(_room, many=True).data)

    def post(self, request):
        """创建房间"""
        room_id = request.data.get('room_id')
        space = request.data.get('space') or 1
        is_hotwater = request.data.get('is_hotwater') or 0
        is_computer = request.data.get('is_computer') or 0
        is_used = request.data.get('space') or 0
        value = request.data.get('value')
        if not room_id or not value:
            return Response({"detail": "房间信息不完整"}, status=status.HTTP_400_BAD_REQUEST)
        _floor = Floor.objects.get(name=int(room_id[0]))
        if Room.objects.filter(room_id=room_id):
            return Response({"detail": "房间已存在"}, status=status.HTTP_400_BAD_REQUEST)
        Room.objects.create(
            room_id=room_id,
            space=space,
            is_hotwater=is_hotwater,
            is_computer=is_computer,
            is_used=is_used,
            value=value,
            floor=_floor
        )
        FreeRoom.objects.filter().first().count += 1
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)

    def delete(self, request):
        """删除指定房间"""
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
        """获取满足条件的全部房间"""
        is_empty = request.GET.get('is_empty')
        if is_empty:
            return Response(RoomSerializer(Room.objects.all(), many=True).data)
        is_used = request.GET.get('is_used') or 2
        space = request.GET.get('space') or 1
        is_hotwater = request.GET.get('is_hotwater') or 2
        is_computer = request.GET.get('is_computer') or 2
        value_l = request.GET.get('input1') or 0
        value_r = request.GET.get('input2') or 999
        _Rooms = Room.objects.filter(
            is_used=is_used,
            space=space,
            is_hotwater=is_hotwater,
            is_computer=is_computer,
            value__in=[value_l, value_r],
        )
        return Response(RoomSerializer(_Rooms, many=True).data)

    def post(self, request):
        """修改房间状态"""
        rid = request.data.get('rid')
        if not rid:
            return Response({"detail": "未获取到房间号"}, status=status.HTTP_400_BAD_REQUEST)
        _room = Room.objects.get(id=rid)
        if not _room:
            return Response({"detail": "房间信息异常"}, status=status.HTTP_400_BAD_REQUEST)
        is_used = 0 if _room.is_used else 1
        _room.update(is_used=is_used)
        if is_used == 0:
            FreeRoom.objects.filter().first().count += 1
        else:
            FreeRoom.objects.filter().first().count -= 1
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)
