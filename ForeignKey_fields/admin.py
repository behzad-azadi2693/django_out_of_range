
from .models import Book,Categry
admin.site.register(cat)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_per_page = 2
    list_display = ['name', 'image_tag']
    
    
    def image_tag(self, obj):
        return mark_safe('<img src="{url}" width="50" height="50" />'.format(url=obj.image.url,))

    def has_change_permission(self, request, obj=None):
        return False    
    
    def has_delete_permission(self, request, obj=None):
        return False

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            kwargs['queryset'] = Category.objects.filter(user = request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(NameOfClassAdmin, self).get_queryset(request)
        return qs.filter(user = request.user)
