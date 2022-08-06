from django.contrib import admin
from .models import User
# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('username', 'email', 'phone_number','is_admin')
    list_filter = ('is_admin', 'username')
    fieldsets = ( #this is for form
        (None,{
            'fields':('username','phone_number','email','password', 'groups', 'user_admin')
            }),
        ('personal info',{
            'fields':('is_active',)
        }),
        ('permission',{
            'fields':('is_admin',)
        }),
    )
    add_fieldsets = (#this is for add_form 
        (None,{
            'fields':('username', 'phone_number', 'email', 'password1', 'password2', 'groups', 'user_permissions')
        }),
    )
    search_fields = ('username', 'phone_number', 'email')
    ordering = ('username',)
    filter_horizontal = ()

    actions = ('make_admin',)
    def make_admin(self, request, queryset):
        queryset.update(is_admin=True)


admin.site.register(User, UserAdmin)

