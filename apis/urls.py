from django.conf.urls import url
from django.urls import path
from .views import TopicApiView, TopicManageApiView

app_name = 'apis'

urlpatterns = [
    url(r'^topic/$', TopicApiView.as_view()),
    url(r'^manage_topic/$', TopicManageApiView.as_view()),
]