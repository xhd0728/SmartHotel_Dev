from rest_framework import serializers

from user.models import User, Level


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = (
            "name",
        )


class UserSerializer(serializers.ModelSerializer):
    level = LevelSerializer()

    class Meta:
        model = User
        fields = (
            "username", "id", "level"
        )
