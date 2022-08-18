from rest_framework.serializers import ModelSerializer
from .models import Blog

class ListSearchSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title', 'descriptions']
