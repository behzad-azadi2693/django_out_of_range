from rest_framework.generics import ListAPIView
from rest_framework import serializers
from .models import Post
from rest_framework.permissions import AllowAny
from elasticsearch import Elasticsearch


class ListSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title', 'body', 'technical_tips']


class ElasticSearch(ListAPIView):
    serializer_class = ListSearchSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self, *args, **kwargs):
        es= Elasticsearch('http://localhost:9200')
        query_param = self.request.GET.get('search_gallery')

        search = es.search(
                index="haystack", 
                query={
                    "multi_match": {
                        'query':query_param,'fields':['title','body','technical_tips', 'tag'],'fuzziness':'AUTO'
                    }
                }
            )

        response = [
                {
                    "id":hit["_source"]["id"].split('.')[-1],
                    "title":hit["_source"]["title"],
                    "body":hit["_source"]["body"],
                    "technical_tips":hit["_source"]["technical_tips"],
                    #"tag":list(hit["_source"]["tag"])[0],
                } 
                for hit in search['hits']['hits']
            ]
 
        return response
 

