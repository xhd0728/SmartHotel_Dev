from rest_framework import serializers

from .models import Comment

from room.serializers import RoomSerializer
from customer.serializers import CustomerSerializer


class CommentSerializer(serializers.ModelSerializer):
    cid = serializers.SerializerMethodField()
    room = RoomSerializer()
    customer = CustomerSerializer()
    create_time = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = Comment
        fields = (
            'cid', 'text', 'star', 'room', 'customer', 'create_time'
        )

    def get_cid(self, obj):
        return obj.id
