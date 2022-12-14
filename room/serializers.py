from rest_framework import serializers

from .models import Room, Floor


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = (
            'name',
        )


class RoomSerializer(serializers.ModelSerializer):
    rid = serializers.SerializerMethodField()
    is_hotwater = serializers.SerializerMethodField()
    is_computer = serializers.SerializerMethodField()
    is_used = serializers.SerializerMethodField()
    floor = FloorSerializer()

    class Meta:
        model = Room
        fields = (
            'rid', 'room_id', 'floor', 'space', 'is_hotwater', 'is_computer', 'is_used', 'value'
        )

    def get_rid(self, obj):
        return obj.id

    def get_is_hotwater(self, obj):
        if obj.is_hotwater:
            return '有'
        else:
            return '无'

    def get_is_computer(self, obj):
        if obj.is_computer:
            return '有'
        else:
            return '无'

    def get_is_used(self, obj):
        if obj.is_used:
            return '有人'
        else:
            return '空闲'
