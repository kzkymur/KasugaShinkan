from django.conf.urls import url
from django.urls import path
from .views import TopicApiView, TopicManageApiView, QuestionApiView, QuestionManageApiView
from .views import password

app_name = 'apis'

urlpatterns = [
    url(r'^password/$', password),
    url(r'^topic/$', TopicApiView.as_view()),
    url(r'^manage_topic/$', TopicManageApiView.as_view()),
    url(r'^question/$', QuestionApiView.as_view()),
    url(r'^manage_question/$', QuestionManageApiView.as_view()),
]