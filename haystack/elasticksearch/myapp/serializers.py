class ListSearchSerializer(serializers.ModelSerializer):
    image_url = serializers.CharField()

    class Meta:
        model = Post
        fields = ['id', 'seo_id', 'title', 'body', 'image_url']
