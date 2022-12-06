from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Order
from .serializers import OrderSerializer

from room.models import Room
from customer.models import Customer


# Create your views here.
class OrderView(APIView):
    def get(self, request):
        oid = request.GET.get('oid')
        if not oid:
            return Response({"detail": "未获取到订单编号"}, status=status.HTTP_400_BAD_REQUEST)
        _order = Order.objects.get(id=oid)
        if not _order:
            return Response({"detail": "该订单不存在"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(OrderSerializer(_order, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        uid = request.data.get('uid')
        rid = request.data.get('rid')
        if not uid or not rid:
            return Response({"detail": "未选择顾客或房间"}, status=status.HTTP_400_BAD_REQUEST)
        _customer = Customer.objects.get(id=uid)
        _room = Room.objects.get(id=rid)
        if not _customer or not _room:
            return Response({"detail": "顾客或房间信息异常"}, status=status.HTTP_400_BAD_REQUEST)
        _pay = request.data.get('pay') or _room.value
        Order.objects.create(room=_room, customer=_customer, pay=_pay)
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)

    def delete(self, request):
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
        return Response(OrderSerializer(Order.objects.all(), many=True).data)

    def post(self, request):
        pass

    def delete(self, request):
        pass
