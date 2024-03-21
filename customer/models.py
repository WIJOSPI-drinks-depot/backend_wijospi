from datetime import datetime
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver

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
        
@receiver(pre_save, sender=Customer)
def check_uniqueness(sender, instance, **kwargs):
    if (instance._state.adding) or ((instance.pk is not None) and (not instance.deleted_at)): # Création et Modification uniquement
        existing_name = sender.objects.filter(
            deleted_at=None,
            name=instance.name,
            surname=instance.surname,
        ).exclude(pk=instance.pk)
        
        existing_contact = sender.objects.filter(
            deleted_at=None,
            contact=instance.contact,
        )
        
        existing_email = sender.objects.filter(
            deleted_at=None,
            email=instance.email,
        )
        
        if existing_name.exists():
            raise ValidationError(
                {'error': 'Un client avec le même nom et prénoms existe déjà.'},
                code='unique_together',
            )
        
        if existing_contact.exists():
            raise ValidationError(
                {'error': 'Un client avec le même contact existe déjà.'},
                code='unique_together',
            )
        
        if existing_email.exists():
            raise ValidationError(
                {'error': 'Un client avec le même email existe déjà.'},
                code='unique_together',
            )