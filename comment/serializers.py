from rest_framework import serializers

from models import Comment


class CommentSerializer(serializers.ModelSerializer):
    cid = serializers.SerializerMethodField()
    create_time = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = Comment
        fields = (
            'cid', 'text', 'star', 'create_time'
        )

        def get_cid(self, obj):
            return obj.id
