from django.db import models
from django.contrib.auth.models import User 
from django.db.models.deletion import CASCADE

# Create your models here.
class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    contact_no = models.CharField(null=True, max_length=20)
    address = models.TextField(null=True, max_length=100)
    gender = models.CharField(null=True, max_length=10)
    dob = models.DateField(null=True, blank=True)
    is_seller = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    has_applied = models.BooleanField(default=False)