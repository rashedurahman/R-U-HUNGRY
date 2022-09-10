from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from watson import search as watson

# Create your models here.
class Restaurant(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    name = models.CharField(max_length=30, unique=True)
    image = models.FileField(upload_to='restaurant/', null=True, blank=True)
    type = models.CharField(max_length=20)

class Menu(models.Model):
    name = models.CharField(max_length=30)
    price = models.IntegerField()
    retaurant = models.ForeignKey(Restaurant, on_delete=CASCADE)
    image = models.FileField(upload_to='menu/', null=True, blank=True)
    is_available = models.BooleanField(default=True)
    category = models.CharField(max_length=30)

watson.register(Restaurant, fields=("name", "type"))
watson.register(Menu, fields=("name", "category"))