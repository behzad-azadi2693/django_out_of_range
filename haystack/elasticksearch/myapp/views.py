from rest_framework.generics import ListAPIView
from rest_framework import serializers
from .models import Post
from rest_framework.permissions import AllowAny
from elasticsearch import Elasticsearch
from .serializers import ListSearchSerializer


class ElasticSearch1(ListAPIView):
    serializer_class = ListSearchSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self, *args, **kwargs):
        es= Elasticsearch('http://username:password@localhost:9200')
        query_param = self.request.GET['search_query']

        search = es.search(
            index = "haystack", 
            query = {
                "bool":{
                    "should":[
                        {"match_phrase":{"title": {"query": query_param}}},
                        {"match":{"title": {"query": query_param,"fuzziness": "AUTO"}}},
                        {"match":{"body": {"query": query_param,"fuzziness": "AUTO:8,15", "operator":"and"}}},
                        {"match":{"seo_id": {"query": query_param,"fuzziness": "AUTO"}}},
                        {"match":{"tags": {"query": query_param,"fuzziness": "AUTO", "operator":"and"}}},
                    ],
                    "filter":[
                        {"term":{"is_active":"true"}},
                        {"term":{"is_remove":"false"}},
                    ],
                    "minimum_should_match":1,
                    "boost":1.0,
                },
            }
        )
        
        response = [
                {
                    "id":hit["_source"]["id"].split('.')[-1],
                    "seo_id":hit["_source"]["seo_id"],
                    "title":hit["_source"]["title"],
                    "body":hit["_source"]["body"],
                    "tags":hit["_source"]["tags"],
                    "image_url":hit["_source"]["image_url"],
                } 
                for hit in search['hits']['hits']
            ]
 
        return response
 


class ElasticSearch2(ListAPIView):
    serializer_class = ListSearchSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self, *args, **kwargs):
        es= Elasticsearch('http://localhost:9200')
        query_param = self.request.GET.get('search_gallery')

        search = es.search(
                index="haystack", 
                query={
                    "multi_match": {
                        'query':query_param,'fields':['title^3','body^2','technical_tips', 'tag'],'fuzziness':'AUTO'
                    }
                }
            )

        response = [
                {
                    "id":hit["_source"]["id"].split('.')[-1],
                    "title":hit["_source"]["title"],
                    "body":hit["_source"]["body"],
                    "technical_tips":hit["_source"]["technical_tips"],
                    "tags":hit["_source"]["tags"],
                    "image_url":hit["_source"]["image_url"],

                } 
                for hit in search['hits']['hits']
            ]
 
        return response
 

    
#---------------------------------------------------or with db--------------------------------------------------    
class ElasticSearchView3(ListAPIView):
    serializer_class = ListSearchSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self, *args, **kwargs):
        es= Elasticsearch('http://boomilia:boomilia@localhost:9200')
        query_param = self.request.GET['q']

        search = es.search(
            index = "haystack", 
            size = 10000,

            query = {
                "bool":{
                    "should":[
                        {"match_phrase":{"title": {"query": query_param}}},
                        {"match":{"title": {"query": query_param,"fuzziness": "AUTO"}}},
                    ],

                },

            },
            
        )
        
        all_id = [hit["_source"]["id"].split('.')[-1] for hit in search['hits']['hits']]
        preserved = Case(*[When(id=field, then=position) for position, field in enumerate(all_id)])

        response = Post.objects.filter(id__in = all_id).order_by(preserved)

        return response


class ElasticSearchView4(ListAPIView):
    serializer_class = ListSearchSerializer
    permission_classes = [AllowAny]
    def get_queryset(self, *args, **kwargs):
        es= Elasticsearch('http://username:passwro@localhost:9200')
        query_param = self.request.GET['q']

        search = es.search(
                index="haystack", 
                query={
                    "multi_match": {
                        'query':query_param,
                        'fields':['title^3'],
                    }
                }
            )

        all_id = [hit["_source"]["id"].split('.')[-1] for hit in search['hits']['hits']]
        preserved = Case(*[When(id=field, then=position) for position, field in enumerate(all_id)])

        response = Post.objects.filter(id__in = all_id).order_by(preserved)

        return response
