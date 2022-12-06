from rest_framework import serializers

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    uid = serializers.SerializerMethodField()
    create_time = serializers.DateTimeField(format="%Y-%m-%d")
    last_time = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = Customer
        fields = (
            'uid', 'name', 'age', 'gender', 'phone_num', 'email', 'level', 'last_time', 'create_time'
        )

    def get_uid(self, obj):
        return obj.id
