from django.contrib import admin
from ecommerce.models import UserProfile ,userAddress ,userNotification ,buyerorder
admin.site.register(UserProfile)
admin.site.register(userAddress)
admin.site.register(userNotification)
admin.site.register(buyerorder)
