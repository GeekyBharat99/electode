from django import forms
from django.contrib.auth.models import User
from ecommerce.models import UserProfile , userAddress

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username','password','email')
class UserProfileForm(forms.ModelForm):
    choices=(('seller','seller'),('buyer','buyer'))
    usertype = forms.CharField(widget=forms.Select(choices=choices))
    class Meta:
        model = UserProfile
        fields = ('mobile','usertype')

class userAddressForm(forms.ModelForm):
    class Meta:
        model = userAddress
        fields = ('houseno','street','ward','city','district','pin','state')
