from .serializers import ListSearchSerializer
from haystack.query import SearchQuerySet
from django.db.models import Q
from rest_framework.generics import ListAPIView


class Index(ListAPIView):
    serializer_class = ListSearchSerializer

    def get_queryset(self, *args, **kwargs):
        name = self.request.GET['q']
        customer = SearchQuerySet().filter(
            Q(descriptions=name) | Q(title=name))
 
        return customer