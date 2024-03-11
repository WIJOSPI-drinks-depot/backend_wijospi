import datetime
from django.db import models

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
        self.updated_at = datetime.now()
        self.save()