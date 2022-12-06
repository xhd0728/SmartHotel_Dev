from rest_framework import serializers

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    cid = serializers.SerializerMethodField()
    create_time = serializers.DateTimeField(format="%Y-%m-%d")
    last_time = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = Customer
        fields = (
            'cid', 'name', 'age', 'gender', 'phone_num', 'email', 'level', 'last_time', 'create_time'
        )

    def get_cid(self, obj):
        return obj.id
