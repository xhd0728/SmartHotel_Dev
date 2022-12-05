from django.db import models
from django.utils import timezone


# Create your models here.
class Comment(models.Model):
    text = models.TextField()
    star = models.SmallIntegerField(default=5)
    create_time = models.DateTimeField(default=timezone.now)
