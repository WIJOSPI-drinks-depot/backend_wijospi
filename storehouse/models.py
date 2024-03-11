from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models

# Create your models here.
class Storehouse(models.Model):
    name = models.CharField(max_length=30)
    contact = models.CharField(max_length=8, validators=[MinLengthValidator(8), MaxLengthValidator(8)])
    type = models.CharField(max_length=15)
    address = models.CharField(max_length=40)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=20, validators=[MinLengthValidator(8), MaxLengthValidator(20)])
    drink_racks = models.ManyToManyField('drink_rack.DrinkRack', through='StorehouseDrinkRack')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)
    
    def __str__(self):
        return(self.name)
    
    def soft_delete(self):
        self.deleted_at = datetime.now()
        self.updated_at = datetime.now()
        self.save()

# relation n à n entre DEPOT et CASIER_BOISSON
class StorehouseDrinkRack(models.Model):
    storehouse = models.ForeignKey(Storehouse, verbose_name=("Dépôt"), on_delete=models.CASCADE)
    drink_rack = models.ForeignKey("drink_rack.DrinkRack", verbose_name=("casier de boisson"), on_delete=models.CASCADE)
    stock_quantity = models.IntegerField() # Il s'agit de la quantité dont dispose le dépôt du casier de boisson
    creation_date = models.DateField() #  La date de création permet de connaître la date de péremption en y ajoutant la durée de vie du casier de boisson

    class Meta:
        unique_together = ('storehouse', 'drink_rack')

    def __str__(self):
        return f"{self.storehouse} - {self.drink_rack}"
    
    # Fonction permettant de calculer la date de péremption du casier de boisson
    def expiration_date(self):
        # Récupérer la durée de vie du casier du modèle drink_rack
        lifespan = self.drink_rack.lifespan
        exp_date = self.creation_date + relativedelta(months=lifespan)
        
        return exp_date
 
 

