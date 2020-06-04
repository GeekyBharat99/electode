from django.db import models
from ecommerce.models import UserProfile
from datetime import datetime
# Create your models here.

class Category(models.Model):
    cat = models.CharField(max_length=30)

    def __str__(self):
        return self.cat

class Products(models.Model):
    product_name = models.CharField(max_length=30)
    product_desc = models.CharField(max_length=50)
    product_price = models.DecimalField(decimal_places=2,max_digits=10)
    added_by_seller = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    product_img = models.ImageField(upload_to='productimage',blank=True)
    product_avail= models.IntegerField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    saveDate = models.DateTimeField(auto_now_add=True)
    modifiedDate = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return self.product_name 
