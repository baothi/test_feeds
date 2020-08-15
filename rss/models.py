from django.db import models
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=255,blank=True,null=True)
    description = models.CharField(max_length=3000,blank=True,null=True)
    website = models.URLField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True )
    publish = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
