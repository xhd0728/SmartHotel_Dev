from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Comment, CommentCount
from .serializers import CommentSerializer

from room.models import Room
from customer.models import Customer


# Create your views here.
class CommentView(APIView):
    def get(self, request):
        """获取指定评论信息"""
        cid = request.GET.get('cid')
        if not cid:
            return Response({"detail": "未获取到评价编号"}, status=status.HTTP_400_BAD_REQUEST)
        _comment = Comment.objects.get(id=cid)
        if not _comment:
            return Response({"detail": "该评论不存在"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(CommentSerializer(_comment, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        """创建或修改评论"""
        phone_num = request.data.get('phone_num')
        room_id = request.data.get('room_id')
        if not phone_num or not room_id:
            return Response({"detail": "未获取到入住信息"}, status=status.HTTP_400_BAD_REQUEST)
        text = request.data.get('text') or "该用户未做出评价，默认五星好评"
        star = request.data.get('star') or 5
        _customer = Customer.objects.get(phone_num=phone_num)
        _room = Room.objects.get(room_id=room_id)
        if not _customer or not _room:
            return Response({"detail": "房间或顾客信息不存在"}, status=status.HTTP_400_BAD_REQUEST)
        cid = request.data.get('cid')
        if cid:
            Comment.objects.update(text=text, star=star, room=_room, customer=_customer)
            return Response({"detail": "ok"}, status=status.HTTP_200_OK)
        Comment.objects.create(text=text, star=star, room=_room, customer=_customer)
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)

    def delete(self, request):
        """删除评价"""
        cid = request.DELETE.get('cid')
        if not cid:
            return Response({"detail": "无此评论信息"}, status=status.HTTP_400_BAD_REQUEST)
        _comment = Comment.objects.get(id=cid)
        if not _comment:
            return Response({"detail": "无此评论信息"}, status=status.HTTP_400_BAD_REQUEST)
        _comment.delete()
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)


class CommentViews(APIView):
    def get(self, request):
        """获取所有评价信息"""
        return Response(CommentSerializer(Comment.objects.all(), many=True).data)
