from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Customer, Level, CustomerCount
from .serializers import CustomerSerializer

from pkg.auth import require_login


# Create your views here.
class CustomerView(APIView):

    @require_login
    def get(self, request):
        """获取顾客信息"""
        uid = request.GET.get('uid')
        if not uid:
            return Response({"detail": "未获取到用户编号"}, status=status.HTTP_400_BAD_REQUEST)
        _customer = Customer.objects.filter(id=uid)
        if not _customer:
            return Response({"detail": "该用户不存在"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(CustomerSerializer(_customer, many=True).data, status=status.HTTP_200_OK)

    @require_login
    def post(self, request):
        """添加或修改顾客"""
        print(request.data)
        name = request.data.get('name')
        age = request.data.get('age') or 0
        gender = request.data.get('gender') or 0
        phone_num = request.data.get('phone_num')
        email = request.data.get('email')
        level = request.data.get('level') or 1
        if not name or not phone_num:
            return Response({"detail": "用户信息填写不完整"}, status=status.HTTP_400_BAD_REQUEST)
        _level = Level.objects.get(id=level)
        uid = request.data.get('uid')
        if uid:
            Customer.objects.filter(id=uid).update(
                name=name,
                age=age,
                gender=gender,
                phone_num=phone_num,
                email=email,
                level=_level
            )
            return Response({"detail": "ok"}, status=status.HTTP_200_OK)
        Customer.objects.create(
            name=name,
            age=age,
            gender=gender,
            phone_num=phone_num,
            email=email,
            level=_level
        )
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)

    @require_login
    def delete(self, request):
        """删除顾客"""
        uid = request.data.get('uid')
        if not uid:
            return Response({"detail": "未获取到顾客信息"}, status=status.HTTP_400_BAD_REQUEST)
        _customer = Customer.objects.filter(id=uid)
        if not _customer:
            return Response({"detail": "未获取到顾客信息"}, status=status.HTTP_400_BAD_REQUEST)
        _customer.delete()
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)


class CustomerViews(APIView):

    @require_login
    def get(self, request):
        """获取顾客列表"""
        is_empty = request.GET.get('is_empty')
        if is_empty == '0':
            return Response(CustomerSerializer(Customer.objects.all(), many=True).data)
        name_or_phone_num = request.GET.get('name_or_phone_num')
        _customer = Customer.objects.filter(name=name_or_phone_num)
        if not _customer:
            _customer = Customer.objects.filter(phone_num=name_or_phone_num)
        if not _customer:
            return Response({"detail": "未查询到符合条件的用户"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(CustomerSerializer(_customer, many=True).data)


class CustomerStatus(APIView):

    @require_login
    def get(self, request):
        """获取顾客信息"""
        customer_count = CustomerCount.objects.get(id=1).count
        return Response({"customer_count": customer_count}, status=status.HTTP_200_OK)
