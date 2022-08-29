from .models import Post
from haystack import indexes
 

class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, use_template=True)
    seo_id = indexes.CharField(model_attr='seo_id')
    title = indexes.CharField(model_attr='title', boost=1)
    body = indexes.CharField(model_attr='body', boost=1)
    tags = indexes.MultiValueField(indexed=True, stored=True)
    image_url = indexes.CharField()
    is_active = indexes.BooleanField(model_attr='is_active')
    is_remove = indexes.BooleanField(model_attr='is_remove')

    class Meta:
        model = Post
        fields = ['text', 'title', 'body', 'tags', 'seo_id', 'image_url', 'is_active', 'is_remove']
 
    def get_model(self):
        return Post
 
    def index_queryset(self, using=None):
        return self.get_model().objects.all()    
    
    def prepare_tags(self, object):
        return [tag.name for tag in object.tags.all()]

    def prepare_image_url(self, object):
        return object.image.path


'''
class PostIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = Post
        fields = ['text', 'title', 'body', 'tag', 'seo_id', 'image', 'is_active', 'is_remove']
 
    def get_model(self):
        return Post
 
    def index_queryset(self, using=None):
        return self.get_model().objects.all()    
'''
