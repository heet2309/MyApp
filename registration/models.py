from django.db import models

class RegistrationTable(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    
    
    class Meta:
        db_table= "registration_table"
        
# class VerifyTable(models.Model):
#     otp = models.IntegerField(max_length=6)
#     email = models.EmailField()
    
# class Meta:
#     db_table = "verify_table"