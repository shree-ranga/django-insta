from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from posts.models import Post

User = get_user_model()


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_comment"
    )
    comment = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_by")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.comment
