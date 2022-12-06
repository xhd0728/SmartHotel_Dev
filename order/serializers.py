from rest_framework import serializers

from customer.serializers import CustomerSerializer
from room.serializers import RoomSerializer

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    oid = serializers.SerializerMethodField()
    room = RoomSerializer()
    customer = CustomerSerializer()
    create_time = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = Order
        fields = (
            'oid', 'room', 'customer', 'pay', 'create_time'
        )

    def get_oid(self, obj):
        return obj.id
