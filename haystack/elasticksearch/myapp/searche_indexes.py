from .models import Customer
from haystack import indexes
 
 
class CustomerIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    descriptions = indexes.CharField(model_attr='descriptions')

    class Meta:
        model = Customer
        fields = ['text', 'title', 'descriptions']
 
    def get_model(self):
        return Customer
 
    def index_queryset(self, using=None):
        return self.get_model().objects.all()