from django.db import models
from django.utils import timezone


# Create your models here.
class Level(models.Model):
    """顾客等级表"""
    name = models.SmallIntegerField(default=0)


class Customer(models.Model):
    """顾客信息表"""
    name = models.CharField(max_length=31)
    age = models.IntegerField(default=0)
    gender = models.SmallIntegerField(default=0)
    phone_num = models.CharField(max_length=11)
    email = models.CharField(max_length=63, blank=True, null=True)
    level = models.ForeignKey(Level, on_delete=models.PROTECT)
    last_time = models.DateTimeField(default=timezone.now)
    create_time = models.DateTimeField(default=timezone.now)


class CustomerCount(models.Model):
    """顾客总数表"""
    count = models.IntegerField(default=0)
