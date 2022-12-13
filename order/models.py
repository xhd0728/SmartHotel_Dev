from django.db import models
from django.utils import timezone
from room.models import Room
from customer.models import Customer


# Create your models here.
class Order(models.Model):
    """订单信息表"""
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    pay = models.DecimalField(max_digits=6, decimal_places=2)
    create_time = models.DateTimeField(default=timezone.now)


class Income(models.Model):
    """酒店收入表"""
    total = models.DecimalField(max_digits=6, decimal_places=2)
