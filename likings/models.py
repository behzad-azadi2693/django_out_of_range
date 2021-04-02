class Post(models.Model):
    image = models.ImageFiled()
    name = models.CharField(max_length=60)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_absulote_url(self):
        return reverse('post:detail', args=[self.id])

    def like_count(self):
        return self.pvote.count()

    def user_can_like(self, user):
        user_like = user.uvote.all()
        qs = user_like.filter(post=self)
        if qs.exists():
            return True
        return False

class Vote(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCAD, related_name='pvote')
    user = models.ForeignKey(User, on_delete=models.CASCAD, related_name='uvote')


    def __str__(self):
        return self.user.username