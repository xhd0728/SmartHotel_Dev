from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Level(models.Model):
    name = models.SmallIntegerField(default=0)


class User(AbstractUser):
    level = models.ForeignKey(Level, on_delete=models.PROTECT)
