from rest_framework import serializers


class ListSearchSerializer(serializers.ModelSerializer):
    image_url = serializers.CharField()
    tags = serializers.ListField()

    class Meta:
        model = Post
        fields = ['id', 'seo_id', 'title', 'tags', 'body', 'image_url']
