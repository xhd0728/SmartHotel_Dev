from django.db import models
from django.utils import timezone


# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=31)
    age = models.IntegerField(default=0)
    gender = models.SmallIntegerField(default=0)
    phone_num = models.CharField(max_length=11)
    email = models.CharField(max_length=63)
    level = models.SmallIntegerField(default=1)
    last_time = models.DateTimeField(default=timezone.now)
    create_time = models.DateTimeField(default=timezone.now)
