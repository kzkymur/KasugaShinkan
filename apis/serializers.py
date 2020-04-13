from rest_framework import serializers
from .models import Topic, Question

import datetime

class TopicSerializer(serializers.ModelSerializer):
    model = Topic

    def create(self, validated_data):
        newTopic = Topic(**validated_data)
        newTopic.created_at = datetime.datetime.now()

        newTopic.save()
        return newTopic

    class Meta:
        model = Topic
        fields='__all__' 
        extra_kwargs = {
            'author' : {'write_only': True},
        }

class QuestionSerializer(serializers.ModelSerializer):
    model = Question

    def create(self, validated_data):
        newQuestion = Question(**validated_data)
        
        newQuestion.save()
        return newQuestion

    class Meta:
        model = Question
        fields='__all__'
