from rest_framework.response import Response

def serch_object_from_model(model, form, filtering_elements):
    serched_topics = serch_objects_from_model(model, form, filtering_elements)
    return serched_topics if isinstance(serched_topics, Response) else serched_topics[0]

def serch_objects_from_model(model, form, filtering_elements):
    filtering_args = {}
    for elem in filtering_elements:
        try:
            filtering_args[elem] = form[elem]
        except:
            return Response("request doesn't have %s vlaue" % elem, status=status.HTTP_400_BAD_REQUEST)
    serched_topics = model.objects.filter(**filtering_args)
    return serched_topics