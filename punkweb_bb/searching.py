from django.db.models import Q
from punkweb_bb.models import Thread


def search_threads(query):
    query_parts = query.split()
    q_objects = Q()
    for part in query_parts:
        q_objects |= Q(title__icontains=part) | Q(content__icontains=part)
    return Thread.objects.filter(q_objects)
