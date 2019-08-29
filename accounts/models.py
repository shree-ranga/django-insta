from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

AbstractUser._meta.get_field("email")._unique = True


class User(AbstractUser):
    profile_image_url = models.ImageField()
    followers = models.ManyToManyField(
        "self", symmetrical=False, through="Follow", related_name="following"
    )
    bio = models.TextField(max_length=150, blank=True)

    # TODO - Add validation. A user cannot follow himself

    def __str__(self):
        return self.username


# Through model(table) for followers/following m2m relationship
class Follow(models.Model):
    following_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower_user"
    )
    follower_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following_user"
    )
    followed_at = models.DateTimeField(default=timezone.now)

    # needed?
    class Meta:
        unique_together = ("following_user", "follower_user")

    def __str__(self):
        return f" {self.follower_user} following {self.following_user}"


class TestImageUpload(models.Model):
    image = models.ImageField()

    def __str__(self):
        return self.image.url
