from rest_framework import serializers
from .models import Topic

class TopicSerializer(serializers.ModelSerializer):
    serial_num = serializers.IntegerField(allow_null=True)

    def create(self, validated_data):
        return Topic.objects.create(**validated_data)

    class Meta:
        model = Topic
        fields='__all__' 