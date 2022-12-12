from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.utils import timezone

from .models import Order, Income
from .serializers import OrderSerializer

from room.models import Room
from customer.models import Customer


# Create your views here.
class OrderView(APIView):
    def get(self, request):
        """获取订单信息"""
        oid = request.GET.get('oid')
        if not oid:
            return Response({"detail": "未获取到订单编号"}, status=status.HTTP_400_BAD_REQUEST)
        _order = Order.objects.get(id=oid)
        if not _order:
            return Response({"detail": "该订单不存在"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(OrderSerializer(_order, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        """新建或编辑订单"""
        phone_num = request.data.get('phone_num')
        room_id = request.data.get('room_id')
        if not phone_num or not room_id:
            return Response({"detail": "未选择顾客或房间"}, status=status.HTTP_400_BAD_REQUEST)
        _customer = Customer.objects.get(phone_num=phone_num)
        _room = Room.objects.get(room_id=room_id)
        if not _customer or not _room:
            return Response({"detail": "顾客或房间信息异常"}, status=status.HTTP_400_BAD_REQUEST)
        _customer.last_time = timezone.now()
        pay = request.data.get('pay') or _room.value
        oid = request.data.get('oid')
        if oid:
            Order.objects.update(room=_room, customer=_customer, pay=pay)
            return Response({"detail": "ok"}, status=status.HTTP_200_OK)
        Order.objects.create(room=_room, customer=_customer, pay=pay)
        Income.objects.filter().first().total += float(pay)
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)

    def delete(self, request):
        """删除订单"""
        oid = request.DELETE.get('oid')
        if not oid:
            return Response({"detail": "未获取到订单编号"}, status=status.HTTP_400_BAD_REQUEST)
        _order = Order.objects.get(id=oid)
        if not _order:
            return Response({"detail": "未获取到订单信息"}, status=status.HTTP_400_BAD_REQUEST)
        _order.delete()
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)


class OrderViews(APIView):
    def get(self, request):
        """获取所有订单信息"""
        return Response(OrderSerializer(Order.objects.all(), many=True).data)
