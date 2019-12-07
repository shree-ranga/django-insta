from django.db import models
from django.utils import timezone
from settings import base
from django.contrib.contenttypes.fields import GenericRelation

from notifications.models import Notification


class Post(models.Model):
    post_image = models.ImageField(null=True, blank=True)
    caption = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(
        base.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="post_by"
    )
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.id} by {self.owner.username}"


# increase the like count or count the number of users liked it?
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_like")
    user = models.ForeignKey(
        base.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="liked_by"
    )
    notification = GenericRelation(Notification)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} liked {self.post.id}"

    class Meta:
        unique_together = ("post", "user")

