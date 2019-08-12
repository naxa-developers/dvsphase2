from django.contrib.gis.db import models

# Create your models here.

class Product (models.Model):
    name=models.CharField(max_length=100)
    quantity=models.IntegerField()

    def is_in_stock(self):
        return self.quantity>0
