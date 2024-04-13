from datetime import datetime
from django.db import models

# Create your models here.
class Supply(models.Model):
    date_time = models.DateTimeField(default=datetime.now)
    storehouse = models.ForeignKey('storehouse.Storehouse', on_delete=models.CASCADE)
    drink_rack = models.ForeignKey('drink_rack.DrinkRack', on_delete=models.CASCADE)
    quantity = models.IntegerField() # Quantité de casiers à approvisionner
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)
    
    def __str__(self):
        return(self.date)
    
    def soft_delete(self):
        self.deleted_at = datetime.now()
        self.save()
    