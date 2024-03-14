from datetime import datetime
from django.db import models

# Create your models here.
class DrinkRack(models.Model):
    name = models.CharField(max_length=40)
    capacity = models.DecimalField(max_digits=5, decimal_places=2) # La contenance d'une bouteille en cl
    lifespan = models.SmallIntegerField(default=12) # La durée de vie est en mois
    price = models.IntegerField() # Il s'agit du prix du casier
    category = models.ForeignKey("category.Category", verbose_name="Catégorie", on_delete=models.CASCADE)
    packaging = models.ForeignKey("packaging.Packaging", verbose_name="Conditionnement", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)
    
    def __str__(self):
        return(self.name)
        
    def soft_delete(self):
        self.deleted_at = datetime.now()
        self.save()