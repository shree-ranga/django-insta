from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from settings import base


class Notification(models.Model):
    NOTIFICATION_TYPE = (("like", "Like"), ("follow", "Follow"))
    sender = models.ForeignKey(
        base.AUTH_USER_MODEL, related_name="notifiction_from", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        base.AUTH_USER_MODEL, related_name="notification_to", on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE)

    def __str__(self):
        return f"{self.sender} -> {self.notification_type} -> {self.receiver}"
