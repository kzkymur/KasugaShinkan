from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Topic
from .renderers import TopicJSONRenderer
from .serializers import TopicSerializer

from .utils import serch_object_from_model

import datetime


class TopicApiView(ListAPIView):
    model = Topic
    permission_classes = (AllowAny, )
    renderer_classes = (TopicJSONRenderer, )
    serializer_class = TopicSerializer

    filtering_elements_at_serch = ['title']

    def get(self, request, format=None):
        topics = self.model.objects.all()
        serialized_topic = self.serializer_class(topics, many=True)
        return Response(serialized_topic.data)

    def post(self, request, format=None):
        serched_topic = serch_object_from_model(self.model, request.POST, self.filtering_elements_at_serch)
        if isinstance(serched_topic, Response):
            return serched_topic
        else:
            serialized_topic = self.serializer_class(serched_topic)
            return Response(serialized_topic.data)


class TopicManageApiView(ListAPIView):
    model = Topic
    permission_classes = (AllowAny, )
    renderer_classes = (TopicJSONRenderer, )
    serializer_class = TopicSerializer

    topic_categories = ['大学', '生活', '先輩']
    filtering_elements_at_edit = ['title', 'author']

    def get(self):
        return Response("this api can't accept GET request", status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format):
        form = request.POST
        form._mutable = True

        if form['category'] == 'edit':
            serched_topic = serch_object_from_model(self.model, form, self.filtering_elements_at_edit)
            if isinstance(serched_topic, Response):
                return serched_topic
            else:
                title = serched_topic.title
                if form['main'] == 'delete':
                    serched_topic.delete()
                    return Response("topic '%s' has deleted" % title, status=status.HTTP_201_CREATED)
                else:
                    serched_topic.main = form['main']
                    serched_topic.updated_at = datetime.datetime.now()
                    return Response("topic '%s' has updated" % title, status=status.HTTP_201_CREATED)

        elif form['category'] in self.topic_categories:
            serializer = self.serializer_class(data=form)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("category isn't in %s" % self.topic_categories, status=status.HTTP_400_BAD_REQUEST)
