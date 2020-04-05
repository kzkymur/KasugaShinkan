from django.conf.urls import url
from django.urls import path
from .views import TopicApiView

app_name = 'apis'

urlpatterns = [
    url(r'^topic/$', TopicApiView.as_view()),
]