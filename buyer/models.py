from django.db import models
from seller.models import Products
from ecommerce.models import User
# Create your models here.

class shoppcart(models.Model):
    class Meta:
        unique_together = (('prodcartid','buyerid'),)
    prodcartid = models.ForeignKey(Products,on_delete=models.CASCADE)
    buyerid = models.ForeignKey(User,on_delete=models.CASCADE)
    

    def __str__(self):
        return self.buyerid

