from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    post_image = models.ImageField(null=True, blank=True)
    caption = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_by")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.post_image} by {self.owner.username}"


# increase the like count or count the number of users liked it?
# class Like(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_like")
#     # is_active = models.BooleanField(default=False)
#     owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_by")
#     created_at = models.DateTimeField(default=timezone.now)

#     # class Meta:
#     #     unique_together = ("post", "owner")

