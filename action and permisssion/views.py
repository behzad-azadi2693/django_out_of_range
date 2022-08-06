
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin


@permission_required('myapp.can_show_views')
@permission_required('myapp.can_read_this')
def my_view(request):
    . 
    . 
    .



class MyClass(PermissionRequiredMixin,ListView):
    . 
    . 
    .
    
    permission_required('myapp.can_show_views')
    permission_required('myapp.can_read_this')