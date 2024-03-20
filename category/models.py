from datetime import datetime
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)
    
    def __str__(self):
        return(self.name)
    
    def soft_delete(self):
        self.deleted_at = datetime.now()
        self.save()
        
@receiver(pre_save, sender=Category)
def check_uniqueness(sender, instance, **kwargs):
    if (instance._state.adding) or ((instance.pk is not None) and (not instance.deleted_at)): # Création et Modification uniquement
        existing_objects = sender.objects.filter(
            deleted_at=None,
            name=instance.name
        ).exclude(pk=instance.pk)
        
        if existing_objects.exists():
            raise ValidationError(
                {'error': 'Une catégorie avec le même nom existe déjà.'},
                code='unique_together',
            )
        
            
            