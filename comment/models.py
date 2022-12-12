from django.db import models
from django.utils import timezone

from room.models import Room
from customer.models import Customer


# Create your models here.
class Comment(models.Model):
    text = models.TextField()
    star = models.SmallIntegerField(default=5)
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    create_time = models.DateTimeField(default=timezone.now)


class CommentCount(models.Model):
    good = models.IntegerField(default=0)
    medium = models.IntegerField(default=0)
    bad = models.IntegerField(default=0)
