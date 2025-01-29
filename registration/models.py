from django.db import models
from django.contrib.auth.models import User  # Importing the default User model


class RegistrationTable(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    class Meta:
        db_table = "registration_table"

class TemporaryTable(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=100,  blank=True, null=True)
    phone = models.CharField(max_length=15,  blank=True, null=True)
    otp = models.CharField(max_length=4)

    class Meta:
        db_table = "temporary_table"
    
class Product(models.Model):
    name = models.CharField(max_length=255,blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "product"

class Cart(models.Model):
    user = models.ForeignKey(RegistrationTable, on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,blank=True, null=True)
    quantity = models.IntegerField(default=1, blank=True, null=True)
    purchased = models.BooleanField(default=False)
   


    def __str__(self):
        return f"{self.product.name} - {self.quantity}" 
    
    class Meta:
        db_table = "cart"       
        
    
