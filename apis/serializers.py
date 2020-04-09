from rest_framework import serializers
from .models import Topic

class TopicSerializer(serializers.ModelSerializer):
    serial_num = serializers.IntegerField(allow_null=True)
    model = Topic

    def create(self, validated_data):
        return self.model.objects.create(**validated_data)

    class Meta:
        model = Topic
        fields='__all__' 