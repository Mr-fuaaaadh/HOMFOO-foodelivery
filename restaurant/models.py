from django.db import models
from user.models import *
# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='restaurants/', null=True)
    owner_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=50)
    location = models.CharField(max_length=100)
    password =  models.CharField(max_length=20)
    status = models.CharField(default="Pending", max_length=10)
    is_open = models.CharField(max_length=20, default="Closed")
    longitude = models.CharField(max_length=20, null=True)
    latitude = models.CharField(max_length=20, null=True)


    def __str__(self):
        return self.name

    class Meta :
        db_table = "Restaurant"


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    image1 = models.ImageField(upload_to='products/')
    image2 = models.ImageField(upload_to='products/')
    image3 = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    offer = models.IntegerField(null=True)
    description = models.TextField(max_length=100)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.name