from .models import Post
from haystack import indexes
 

class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title', boost=1)
    body = indexes.CharField(model_attr='body', boost=1)
    tag = indexes.MultiValueField(indexed=True, stored=True)
    technical_tips = indexes.CharField(model_attr='technical_tips')
    
    class Meta:
        model = Post
        fields = ['text', 'title', 'body', 'tag', 'technical_tips']
 
    def get_model(self):
        return Post
 
    def index_queryset(self, using=None):
        return self.get_model().objects.all()    
    
    def prepare_tag(self, object):
        return [tag.name for tag in object.tag.all()]
