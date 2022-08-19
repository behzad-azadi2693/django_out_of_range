from .serializers import ListSearchSerializer
from haystack.query import SearchQuerySet
from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny


class ElasticSearch1(ListAPIView):
    serializer_class = ListSearchSerializer

    def get_queryset(self, *args, **kwargs):
        name = self.request.GET['q']
        customer = SearchQuerySet().filter(
            Q(descriptions__fuzzy=name) | Q(title__fuzzy=name))
 
        return customer


class ElasticSearch2(ListAPIView):
    serializer_class = ListSearchSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self, *args, **kwargs):
        es= Elasticsearch('http://localhost:9200')
        query_param = self.request.GET.get('q')

        resp = es.search(
                index="haystack", 
                query={
                    "multi_match": {
                        'query':query_param,'fields':['title','descriptions'],'fuzziness':'AUTO'
                    }
                }
            )
        
        all = [
                {
                    "id":hit["_source"]["id"].split('.')[-1],
                    "title":hit["_source"]["title"],
                    "descriptions":hit["_source"]["descriptions"]
                } 
                for hit in resp['hits']['hits']
            ]
 
        return all
