from django.db import models
from django.contrib.auth.hashers import make_password, check_password
# Create your models here.



class Customer(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        self.password = check_password(raw_password)





class Banner(models.Model):
    image = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta :
        db_table = "Banner"





class Category(models.Model):
    name = models.CharField(max_length=25)
    image = models.ImageField(upload_to='images/')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta :
        db_table = "Category"


