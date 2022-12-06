from rest_framework import serializers

from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    rid = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = (
            'rid', 'room_id', 'space', 'is_hotwater', 'is_computer', 'value'
        )

    def get_rid(self, obj):
        return obj.id
