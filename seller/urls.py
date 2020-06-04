from django.urls import path
from seller import views

app_name = 'seller'

urlpatterns=[
    path('sellerapp/',views.sellerapp),
    path('addproduct/',views.addproduct),
    path('addcategory/',views.addcategory),
    path('addedproduct/',views.addedproduct),
    path('modifyproduct/<int:id>/',views.modifyproduct,name='modifyproduct'),
    path('sellernotifications/',views.sellernotifications),
    path('createnotifications/',views.createnotifications),
    path('sellerorders/',views.sellerorders),
    path('sellershippcall/<int:id>',views.sellershippcall,name = 'sellershippcall'),
]
