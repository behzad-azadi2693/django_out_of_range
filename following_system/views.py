from .models import Relation
from django.contrib.auth.models import User
from django.http import JsonResponse

def profile(request, username):
    user = User.objects.get(username = username)
    is_follow = False
    relation = Relation.object.filter(from_user=request.user, to_user=user)
    if relation.exists():
        is_follow = True

    context = {
        'user':user,
        'is_follow':is_follow
    }
    return render(request, 'profile.html', context)

@login_required
def follow(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        following = get_object_or_404(User, pk=user_id)
        check_relation = Relation.objects.filter(from_user = request.user, to_user=following)
        if check_relation.exists():
            return JsonResponse({'status':'exists'})

        else:
            Relation(from_user=request.user, to_user=following).save()
            return JsonResponse({'status':'ok'})


@login_required
def unfollow(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        following = get_object_or_404(User, pk=user_id)        
        check_relation = Relation.objects.filter(from_user = request.user, to_user=following)
        if check_relation.exists():
            check_relation.delete()
            return JsonResponse({'status':'ok'})
        else:
            return JsonResponse({'status':'notexists'})