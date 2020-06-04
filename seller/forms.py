from django import forms
from seller.models import Category,Products

class sellerform(forms.Form):
    name = forms.CharField()
    desc = forms.CharField()
    price = forms.DecimalField()
    sellby = forms.CharField()
    img = forms.ImageField()
    avail = forms.IntegerField()
    Category =forms.Select()
    savedate = forms.DateTimeField()
    modifieddate = forms.DateTimeField()
