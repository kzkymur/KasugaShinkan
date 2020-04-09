from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Topic
from .renderers import TopicJSONRenderer
from .serializers import TopicSerializer

from .utils import serch_object_from_model


class TopicApiView(ListAPIView):
    model = Topic
    permission_classes = (AllowAny, )
    renderer_classes = (TopicJSONRenderer, )
    serializer_class = TopicSerializer

    filtering_elements_at_serching = ['title']

    def get(self, request, format=None):
        topics = self.model.objects.all()
        serialized_topic = self.serializer_class(topics, many=True)
        return Response(serialized_topic.data)

    def post(self, request, format=None):
        serched_topic = serch_object_from_model(self.model, request.POST, self.filtering_elements_at_serching)
        if isinstance(serched_topic, Response):
            return serched_topic
        else:
            serialized_topic = self.serializer_class(serched_topic)
            if serialized_topic.is_valid():
                return Response(serialized_topic.data)
            else:
                return Response("request form doesn't match any topics", status=status.HTTP_400_BAD_REQUEST)


class ManageTopicApiView(ListAPIView):
    model = Topic
    permission_classes = (AllowAny, )
    renderer_classes = (TopicJSONRenderer, )
    serializer_class = TopicSerializer

    topic_categories = ['大学', '生活', '先輩']
    filtering_elements_at_editting = ['title', 'author']

    def get(self):
        return Response("this api can't accept GET request", status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format):
        form = request.POST
        form._mutable = True
        if form['category'] == 'edit':
            serched_topic = serch_object_from_model(self.model, form, self.filtering_elements_at_editting)
            serialized_topic = self.serializer_class(serched_topic)
            if serialized_topic.is_valid():
                return Response(serialized_topic.data)
            else:
                return Response("request form doesn't match any topics", status=status.HTTP_400_BAD_REQUEST)

            if form['main'] == 'delete':
                filtering_args = {}
                for elem in self.filtering_elements_at_editting:
                    try:
                        filtering_args[elem] = form[elem]
                    except:
                        return Response("request doesn't have %s vlaue" % elem, status=status.HTTP_400_BAD_REQUEST)
                delete_topic = self.model.objects.filter(**filtering_args)[0]
                try:
                    delete_topic.delete()
                except:
                    return Response("request doesn't match any topics", status=status.HTTP_400_BAD_REQUEST)
                return Response("topic '%s' has deleted" % delete_topic['title'], status=status.HTTP_201_CREATED)
            
            else:

            serializer = self.serializer_class(data=form)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
