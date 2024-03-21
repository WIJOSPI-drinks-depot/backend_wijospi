from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver

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
        self.save()

@receiver(pre_save, sender=Storehouse)
def check_uniqueness(sender, instance, **kwargs):
    if (instance._state.adding) or ((instance.pk is not None) and (not instance.deleted_at)): # Création et Modification uniquement
        existing_name = sender.objects.filter(
            deleted_at=None,
            name=instance.name,
        ).exclude(pk=instance.pk)
        
        existing_contact = sender.objects.filter(
            deleted_at=None,
            contact=instance.contact,
        ).exclude(pk=instance.pk)
        
        existing_email = sender.objects.filter(
            deleted_at=None,
            email=instance.email,
        ).exclude(pk=instance.pk)
        
        if existing_name.exists():
            raise ValidationError(
                {'error': 'Un dépôt avec le même nom existe déjà.'},
                code='unique_together',
            )
        
        if existing_contact.exists():
            raise ValidationError(
                {'error': 'Un dépôt avec le même contact existe déjà.'},
                code='unique_together',
            )
        
        if existing_email.exists():
            raise ValidationError(
                {'error': 'Un dépôt avec le même email existe déjà.'},
                code='unique_together',
            )

# relation n à n entre DEPOT et CASIER_BOISSON
class StorehouseDrinkRack(models.Model):
    storehouse = models.ForeignKey(Storehouse, verbose_name=("Dépôt"), on_delete=models.CASCADE)
    drink_rack = models.ForeignKey("drink_rack.DrinkRack", verbose_name=("casier de boisson"), on_delete=models.CASCADE)
    stock_quantity = models.IntegerField() # Il s'agit de la quantité dont dispose le dépôt du casier de boisson
    creation_date = models.DateField() #  La date de création permet de connaître la date de péremption en y ajoutant la durée de vie du casier de boisson
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)

    def __str__(self):
        return f"{self.storehouse} - {self.drink_rack}"
    
    def soft_delete(self):
        self.deleted_at = datetime.now()
        self.save()
        
    # Fonction permettant de calculer la date de péremption du casier de boisson
    def expiration_date(self):
        # Récupérer la durée de vie du casier du modèle drink_rack
        lifespan = self.drink_rack.lifespan
        
        exp_date = self.creation_date + relativedelta(months=lifespan)
        
        return exp_date
 
# Vérifier s'il n'existe pas déjà une relation entre un dépôt et un casier de boisson
# avant d'enregistrer une nouvelle relation
# tout en excluant les relations supprimées (suppression logique) de cette vérification
@receiver(pre_save, sender=StorehouseDrinkRack)
def check_unique_on_create(sender, instance, **kwargs):
    if instance._state.adding:
        existing_objects = sender.objects.filter(
            deleted_at=None,
            storehouse=instance.storehouse,
            drink_rack=instance.drink_rack,
            creation_date=instance.creation_date
        ).exclude(pk=instance.pk)
    
        if existing_objects.exists():
            raise ValidationError(
                {'error': 'Une entrée avec les mêmes valeurs existe déjà.'},
                code='unique_together',
            )
