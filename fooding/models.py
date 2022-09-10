from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from seller.models import Menu, Restaurant
from django.db import models

# Create your models here.
class Cart(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=CASCADE)
    user = models.ForeignKey(User, on_delete=CASCADE)
    item = models.ForeignKey(Menu, on_delete=CASCADE)
    quantity = models.IntegerField()
    total_price = models.IntegerField()

class Order(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=CASCADE)
    user = models.ForeignKey(User, on_delete=CASCADE)
    item = models.ForeignKey(Menu, on_delete=CASCADE)
    quantity = models.IntegerField()
    total_price = models.IntegerField()
    status = models.CharField(max_length=10, default="Pending")
    is_reviewed = models.BooleanField(default=False)


class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=CASCADE)
    item = models.ForeignKey(Menu, on_delete=CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=CASCADE)
    review = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now_add=True, null=True)