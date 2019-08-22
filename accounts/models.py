from django.db import models
from django.contrib.auth.models import AbstractUser

AbstractUser._meta.get_field("email")._unique = True


class User(AbstractUser):
    profile_image_url = models.ImageField(default="default.jpg")
    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="following"
    )
    bio = models.TextField(max_length=150, blank=True)

    # TODO - Add validation. A user cannot follow himself

    def __str__(self):
        return self.username


class TestImageUpload(models.Model):
    image = models.ImageField()

    def __str__(self):
        return self.image.url
