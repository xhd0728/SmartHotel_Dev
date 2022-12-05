from django.db import models
from django.utils import timezone
from room.models import Room
from customer.models import Customer


# Create your models here.
class Order(models.Model):
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    pay = models.DecimalField(max_digits=4, decimal_places=2)
    create_time = models.DateTimeField(default=timezone.now)
