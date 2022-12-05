from django.db import models


# Create your models here.
class Room(models.Model):
    room_id = models.CharField(max_length=4, default=000)
    space = models.SmallIntegerField(default=1)
    is_hotwater = models.SmallIntegerField(default=0)
    is_computer = models.SmallIntegerField(default=0)
    value = models.DecimalField(max_digits=4, decimal_places=2)
