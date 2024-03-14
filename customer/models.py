from datetime import datetime
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    contact = models.CharField(max_length=8, validators=[MinLengthValidator(8), MaxLengthValidator(8)])
    address = models.CharField(max_length=40)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=20, validators=[MinLengthValidator(8), MaxLengthValidator(20)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)
    
    def __str__(self):
        return(f"{self.surname} {self.name}")
    
    def soft_delete(self):
        self.deleted_at = datetime.now()
        self.save()