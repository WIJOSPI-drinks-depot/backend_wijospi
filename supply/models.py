from datetime import datetime
from django.db import models

# Create your models here.
class Supply(models.Model):
    date = models.DateField(default=datetime.now)
    storehouse = models.ForeignKey('storehouse.Storehouse', on_delete=models.CASCADE)
    drink_racks = models.ManyToManyField('drink_rack.DrinkRack', through='SupplyDrinkRack')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)
    
    def __str__(self):
        return(self.date)
    
    def soft_delete(self):
        self.deleted_at = datetime.now()
        self.updated_at = datetime.now()
        self.save()

# Relation n à n entre APPROVISIONNEMENT et CASIER_BOISSON
class SupplyDrinkRack(models.Model):
    supply = models.ForeignKey(Supply, verbose_name=("Approvisionnement"), on_delete=models.CASCADE)
    drink_rack = models.ForeignKey("drink_rack.DrinkRack", verbose_name=("Casier de boisson"), on_delete=models.CASCADE)
    supply_quantity = models.IntegerField() # La quantité approvisionnée du casier de boisson
    
    class Meta:
        unique_together = ('supply', 'drink_rack')
    
    def __str__(self):
        return f"{self.supply} - {self.drink_rack}"
    