from .PASS import PASSWORD, KEY
from django.http import JsonResponse
from rest_framework.generics import ListAPIView, RetrieveAPIView

class Password(ListAPIView):
    def get(self, request):
        return Response("this api can't accept GET request", status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        form = request.POST
        if self.check_password(form):
            return_json = {
                'result': True,
                'key': KEY,
            }
        else:
            return_json = {'result': False}
        return JsonResponse(return_json)

    def check_password(self, form):
        return form['password'] == PASSWORD

def check_key(form):
    return form['key'] == KEY

def get_all_objects(model):
    return model.objects.all()


from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Topic, Question
from .renderers import TopicJSONRenderer, QuestionJSONRenderer, ResponseRenderer
from .serializers import TopicSerializer, QuestionSerializer

from .utils import serch_object_from_model, serch_objects_from_model

import datetime
import json


topic_categories = ['大学', '生活', '先輩']


class TopicApiView(ListAPIView):
    model = Topic
    permission_classes = (AllowAny, )
    renderer_classes = (TopicJSONRenderer, )
    serializer_class = TopicSerializer

    filtering_elements_at_serch = ['title']

    def get(self, request, format=None):
        all_objs = get_all_objects(self.model)
        serialized_objs = self.serializer_class(all_objs, many=True)
        return Response(serialized_objs.data)

    def post(self, request, format=None):
        serched_obj = serch_object_from_model(self.model, request.POST, self.filtering_elements_at_serch)
        if isinstance(serched_obj, Response):
            return serched_obj
        else:
            serialized_obj = self.serializer_class(serched_obj)
            return Response(serialized_obj.data)


class TopicManageApiView(ListAPIView):
    model = Topic
    permission_classes = (AllowAny, )
    renderer_classes = (ResponseRenderer, )
    serializer_class = TopicSerializer

    filtering_elements_at_edit = ['title', 'author']

    def get(self, request):
        return Response("this api can't accept GET request", status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        form = request.POST
        form._mutable = True

        if check_key(form):
            form.pop('key')
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
                        # main, youtube_link は undefined なら変更なし
                        if form['main']:
                            serched_topic.main = form['main']
                        if form['youtube_link']:
                            serched_topic.youtube_link = form['youtube_link']
                        serched_topic.updated_at = datetime.datetime.now()
                        serched_topic.save()
                        return Response("topic '%s' has updated" % title, status=status.HTTP_201_CREATED)

            elif form['category'] in topic_categories:
                if 'question_main' in form:
                    # question.main と topic.main は異なるのでそこの修正
                    question_form = {'main':form['question_main']}
                    QuestionManageApiView().delete(question_form)
                    form.pop('question_main')
                serializer = self.serializer_class(data=form)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("category isn't in %s" % topic_categories, status=status.HTTP_400_BAD_REQUEST)
        else: 
            return Response("key is invalid" , status=status.HTTP_400_BAD_REQUEST)



class QuestionApiView(ListAPIView):
    model = Question
    permission_classes = (AllowAny, )
    renderer_classes = (QuestionJSONRenderer, )
    serializer_class = QuestionSerializer

    filtering_elements_at_serch = ['category']

    def get(self, request, format=None):
        all_objs = get_all_objects(self.model)
        serialized_objs = self.serializer_class(all_objs, many=True)
        return Response(serialized_objs.data)

    def post(self, request, format=None):
        serched_objs = serch_objects_from_model(self.model, request.POST, self.filtering_elements_at_serch)
        if isinstance(serched_objs, Response):
            return serched_objs
        else:
            serialized_objs = self.serializer_class(serched_objs)
            return Response(serialized_objs.data)


class QuestionManageApiView(ListAPIView):
    model = Question
    permission_classes = (AllowAny, )
    renderer_classes = (ResponseRenderer, )
    serializer_class = QuestionSerializer

    filtering_elements_at_del = ['main']

    def get(self, request):
        return Response("this api can't accept GET request", status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        form = request.POST
        form._mutable = True
        mode = int(form['mode'])
        form.pop('mode')

        # mode 0 : add
        #      1 : delete

        if mode:
            if check_key(form):
                if 'delete_questions' in form:
                    for question in json.loads(form['delete_questions']):
                        delete_result = self.delete(question)
                        if delete_result.status_code != 201:
                            return delete_result
                    return Response('questions deleted', status=status.HTTP_201_CREATED)
                else:
                    return self.delete(form)
            else:
                return Response("key is invalid" , status=status.HTTP_400_BAD_REQUEST)
        else:
            if form['category'] in topic_categories:
                serializer = self.serializer_class(data=form)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("category isn't in %s" % topic_categories, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, form):
        serched_question = serch_object_from_model(self.model, form, self.filtering_elements_at_del)
        if isinstance(serched_question, Response):
            return serched_question
        else:
            main = serched_question.main
            serched_question.delete()
            return Response("topic '%s' has deleted" % main, status=status.HTTP_201_CREATED)
            