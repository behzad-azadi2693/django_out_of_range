def detail(request, pk):
    post = Post.objects.get(pk=pk)
    can_like = False
    if request.user.is_authenticated:
        if post.user_can_like(request.user):
            can_like=True

    return render(request, 'detail.html', {'post':post, 'can_like':can_like})


@login_required
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like = vote(post=post, user=request.user)
    like.save()
    message.success(request, 'liking success', 'success')
    return redirec('post:detail', post.id)