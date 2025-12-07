from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    POST_TYPES = [
        ('help', ' Demande d’aide'),
        ('event', ' Événement'),
        ('announcement', ' Annonce'),
        ('lost', ' Objet perdu/trouvé'),
        ('other', ' Autre'),
    ]
    @property
    def top_comments(self):
        """Commentaires de premier niveau uniquement"""
        return self.comments.filter(parent__isnull=True).order_by('-created_at')


    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    post_type = models.CharField(max_length=20, choices=POST_TYPES, default='other')
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_post_type_display()})"

    def total_likes(self):
        return self.likes.count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} aime {self.post.title}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name="replies", on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def is_reply(self):
        return self.parent is not None
