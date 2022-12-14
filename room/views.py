from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Room, Floor, FreeRoom
from .serializers import RoomSerializer

from django.db.models import Q

from pkg.auth import require_login


# Create your views here.
class RoomView(APIView):

    @require_login
    def get(self, request):
        """获取指定房间信息"""
        rid = request.GET.get('rid')
        if not rid:
            return Response({"detail": "未获取到房间编号"}, status=status.HTTP_400_BAD_REQUEST)
        _room = Room.objects.filter(id=rid)
        if not _room:
            return Response({"detail": "房间信息异常"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(RoomSerializer(_room, many=True).data)

    @require_login
    def post(self, request):
        """创建房间"""
        room_id = request.data.get('room_id')
        space = request.data.get('space') or 1
        is_hotwater = request.data.get('is_hotwater') or 0
        is_computer = request.data.get('is_computer') or 0
        is_used = request.data.get('is_used') or 0
        value = request.data.get('value')
        floor = request.data.get('floor') or 1
        if not room_id or not value:
            return Response({"detail": "房间信息不完整"}, status=status.HTTP_400_BAD_REQUEST)
        _floor = Floor.objects.get(name=floor)
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
        # 触发器操作，在数据库中实现
        # _free_room_count=FreeRoom.objects.get(id=1)
        # _free_room_total=FreeRoom.objects.get(id=2)
        # _free_room_count.count += 1
        # _free_room_total.count += 1
        # _free_room_count.save()
        # _free_room_total.save()
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)

    @require_login
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

    @require_login
    def get(self, request):
        """获取满足条件的全部房间"""
        is_empty = request.GET.get('is_empty')
        if is_empty == '0':
            return Response(RoomSerializer(Room.objects.all(), many=True).data)
        q = Q()
        q.connector = 'AND'
        _is_used = request.GET.get('is_used') or '2'
        if _is_used == '0':
            q.children.append(('is_used', 0))
        elif _is_used == '1':
            q.children.append(('is_used', 1))
        else:
            q_is_used = Q()
            q_is_used.connector = 'OR'
            q_is_used.children.append(('is_used', 0))
            q_is_used.children.append(('is_used', 1))
            q.add(q_is_used, 'AND')
        _space = request.GET.get('space') or '1'
        if _space == '1':
            q.children.append(('space', 1))
        elif _space == '2':
            q.children.append(('space', 2))
        else:
            q.children.append(('space', 3))
        _is_hotwater = request.GET.get('is_hotwater') or 2
        if _is_hotwater == '0':
            q.children.append(('is_hotwater', 0))
        elif _is_hotwater == '1':
            q.children.append(('is_hotwater', 1))
        else:
            q_is_hotwater = Q()
            q_is_hotwater.connector = 'OR'
            q_is_hotwater.children.append(('is_hotwater', 0))
            q_is_hotwater.children.append(('is_hotwater', 1))
            q.add(q_is_hotwater, 'AND')
        _is_computer = request.GET.get('is_computer') or 2
        if _is_computer == '0':
            q.children.append(('is_computer', 0))
        elif _is_computer == '1':
            q.children.append(('is_computer', 1))
        else:
            q_is_computer = Q()
            q_is_computer.connector = 'OR'
            q_is_computer.children.append(('is_computer', 0))
            q_is_computer.children.append(('is_computer', 1))
            q.add(q_is_computer, 'AND')
        _value_l = request.GET.get('input1') or 0
        _value_r = request.GET.get('input2') or 999
        q.children.append(('value__gte', _value_l))
        q.children.append(('value__lte', _value_r))
        _Rooms = Room.objects.filter(q)
        return Response(RoomSerializer(_Rooms, many=True).data)

    @require_login
    def post(self, request):
        """修改房间状态"""
        rid = request.data.get('rid')
        if not rid:
            return Response({"detail": "未获取到房间号"}, status=status.HTTP_400_BAD_REQUEST)
        _room = Room.objects.get(id=rid)
        if not _room:
            return Response({"detail": "房间信息异常"}, status=status.HTTP_400_BAD_REQUEST)
        is_used = 0 if _room.is_used else 1
        _room.is_used = is_used
        _room.save()
        # 触发器操作，在数据库中实现
        # _free_room_count = FreeRoom.objects.get(id=1)
        # if is_used == 0:
        #     _free_room_count.count += 1
        # else:
        #     _free_room_count.count -= 1
        # _free_room_count.save()
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)


class RoomStatus(APIView):

    @require_login
    def get(self, request):
        """酒店房间状态信息"""
        free_room = FreeRoom.objects.get(id=1).count
        total_room = FreeRoom.objects.get(id=2).count
        return Response({"free_room": free_room, "total_room": total_room}, status=status.HTTP_200_OK)
