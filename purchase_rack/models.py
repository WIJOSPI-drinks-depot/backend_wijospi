from datetime import datetime
from django.db import models

# Create your models here.
class PurchaseRack(models.Model):
    capacity = models.IntegerField() # Le nombre de place disponible dans le casier
    quantity = models.IntegerField() # Le nombre de casier commandé
    purchase = models.ForeignKey('purchase.Purchase', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)
    
    def __str__(self):
        return(self.capacity)
    
    def soft_delete(self):
        self.deleted_at = datetime.now()
        self.save()

# Relation n à n entre CASIER_ACHAT et CASIER_BOISSON
class PurchaseRackDrinkRack(models.Model):
    purchase_rack = models.ForeignKey(PurchaseRack, verbose_name="Casier d'achat", on_delete=models.CASCADE)
    drink_rack = models.ForeignKey("drink_rack.DrinkRack", verbose_name=("Casier de boisson"), on_delete=models.CASCADE)
    drink_quantity = models.IntegerField() # Quantité de boisson choisie du casier de boisson
    
    class Meta:
        unique_together = ('purchase_rack', 'drink_rack')
    
    def __str__(self):
        return f"{self.purchase_rack} - {self.drink_rack}"