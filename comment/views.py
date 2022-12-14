from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Comment, CommentCount
from .serializers import CommentSerializer

from room.models import Room
from customer.models import Customer

from pkg.auth import require_login


# Create your views here.
class CommentView(APIView):

    @require_login
    def get(self, request):
        """获取指定评论信息"""
        cid = request.GET.get('cid')
        if not cid:
            return Response({"detail": "未获取到评价编号"}, status=status.HTTP_400_BAD_REQUEST)
        _comment = Comment.objects.filter(id=cid)
        if not _comment:
            return Response({"detail": "该评论不存在"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(CommentSerializer(_comment, many=True).data, status=status.HTTP_200_OK)

    @require_login
    def post(self, request):
        """创建或修改评论"""
        phone_num = request.data.get('phone_num')
        room_id = request.data.get('room_id')
        if not phone_num or not room_id:
            return Response({"detail": "未获取到入住信息"}, status=status.HTTP_400_BAD_REQUEST)
        if not Customer.objects.filter(phone_num=phone_num) or not Room.objects.filter(room_id=room_id):
            return Response({"detail": "房间或顾客信息不存在"}, status=status.HTTP_400_BAD_REQUEST)
        text = request.data.get('text') or "该用户未做出评价，默认五星好评"
        star = request.data.get('star') or 5
        _customer = Customer.objects.get(phone_num=phone_num)
        _room = Room.objects.get(room_id=room_id)
        cid = request.data.get('cid')
        if cid:
            Comment.objects.filter(id=cid).update(
                text=text,
                star=star,
                room=_room,
                customer=_customer
            )
            return Response({"detail": "ok"}, status=status.HTTP_200_OK)
        Comment.objects.create(
            text=text,
            star=star,
            room=_room,
            customer=_customer
        )
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)

    @require_login
    def delete(self, request):
        """删除评价"""
        cid = request.data.get('cid')
        if not cid:
            return Response({"detail": "未获取到评价编号"}, status=status.HTTP_400_BAD_REQUEST)
        _comment = Comment.objects.filter(id=cid)
        if not _comment:
            return Response({"detail": "无评论信息"}, status=status.HTTP_400_BAD_REQUEST)
        _comment.delete()
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)


class CommentViews(APIView):

    @require_login
    def get(self, request):
        """获取所有评价信息"""
        return Response(CommentSerializer(Comment.objects.all(), many=True).data)


class CommentStatus(APIView):

    @require_login
    def get(self, request):
        """获取评论数量"""
        comment_good = CommentCount.objects.get(id=1).good
        comment_medium = CommentCount.objects.get(id=1).medium
        comment_bad = CommentCount.objects.get(id=1).bad
        total = {
            'comment_good': comment_good,
            'comment_medium': comment_medium,
            'comment_bad': comment_bad
        }
        return Response(total, status=status.HTTP_200_OK)
