from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10)
    usertype = models.CharField(max_length=20)
    def __str__(self):
        return self.user.username

class userAddress(models.Model):
    uaddid = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    houseno = models.CharField(max_length=20)
    street = models.CharField(max_length = 100)
    ward = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    pin = models.CharField(max_length=6)
    state = models.CharField(max_length=50)

    def __str__(self):
        return self.pin

class userNotification(models.Model):
    userid = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    message = models.CharField(max_length = 1000)
    tim = models.DateTimeField(auto_now_add=True)

class buyerorder(models.Model):
    userid = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    buyerid = models.IntegerField()
    productname = models.CharField(max_length = 50)
    productprice = models.DecimalField(decimal_places=2,max_digits=10)
    productqty = models.IntegerField()
    buyermobile = models.CharField(max_length=10)
    buyeraddress = models.CharField(max_length=150)
    productimage = models.ImageField(blank=True)
    status = models.CharField(max_length=50)
    tim = models.DateTimeField(auto_now_add=True)
