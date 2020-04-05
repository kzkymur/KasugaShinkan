from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Topic
from .renderers import TopicJSONRenderer
from .serializers import TopicSerializer


class TopicApiView(ListAPIView):
    model = Topic
    queryset = Topic.objects.all()
    permission_classes = (AllowAny, )
    renderer_classes = (TopicJSONRenderer, )
    serializer_class = TopicSerializer


class TopicRetrieveApiView(RetrieveAPIView):
    permission_classes = (AllowAny, )
    renderer_classes = (TopicJSONRenderer, )
    serializer_class = TopicSerializer

    def retrieve(self, request, Topic_id, *args, **kwargs):
        topic = Topic.objects.get(id=Topic_id)
        serializer = self.serializer_class(topic)

        return Response(serializer.data, status=status.HTTP_200_OK)