import json
from rest_framework.renderers import JSONRenderer


class TopicJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = json.dumps({
                'topic': data,
            },ensure_ascii=False)
        return response