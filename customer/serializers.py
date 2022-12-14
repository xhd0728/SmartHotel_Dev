from rest_framework import serializers

from .models import Customer, Level


class LevelSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Level
        fields = (
            'name',
        )

    def get_name(self, obj):
        if obj.name == 1:
            return '普通会员'
        elif obj.name == 2:
            return '超级会员'
        else:
            return '至尊会员'


class CustomerSerializer(serializers.ModelSerializer):
    level = LevelSerializer()
    uid = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    create_time = serializers.DateTimeField(format="%Y-%m-%d")
    last_time = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = Customer
        fields = (
            'uid', 'name', 'age', 'gender', 'phone_num', 'email', 'level', 'last_time', 'create_time'
        )

    def get_uid(self, obj):
        return obj.id

    def get_gender(self, obj):
        if obj.gender == 0:
            return '未指定'
        elif obj.gender == 1:
            return '男'
        else:
            return '女'
