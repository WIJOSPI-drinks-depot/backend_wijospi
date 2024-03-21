from datetime import datetime
from django.db import models

# Create your models here.
class Purchase(models.Model):
    date_time = models.DateTimeField(default=datetime.now)
    customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE)
    storehouse = models.ForeignKey('storehouse.Storehouse', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)
    
    def __str__(self):
        return(f"{self.customer} - {self.date_time} - {self.storehouse}")
    
    def soft_delete(self):
        self.deleted_at = datetime.now()
        self.save()