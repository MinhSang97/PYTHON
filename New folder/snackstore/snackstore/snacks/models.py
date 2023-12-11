from django.db import models

# Create your models here.
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
