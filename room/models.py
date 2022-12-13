from django.db import models


# Create your models here.
class Floor(models.Model):
    """楼层表"""
    name = models.SmallIntegerField(default=1)


class Room(models.Model):
    """房间信息表"""
    room_id = models.CharField(max_length=4, default='000')
    space = models.SmallIntegerField(default=1)
    is_hotwater = models.SmallIntegerField(default=0)
    is_computer = models.SmallIntegerField(default=0)
    is_used = models.SmallIntegerField(default=0)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    floor = models.ForeignKey(Floor, on_delete=models.PROTECT)


class FreeRoom(models.Model):
    """空闲房间表"""
    count = models.IntegerField(default=0)
