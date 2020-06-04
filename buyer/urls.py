from django.urls import path
from buyer import views

app_name = 'buyer'

urlpatterns=[
    # path('buyerapp/',views.buyerapp,name='buyerapp'),
    path('',views.buyerapp,name='buyerapp'),
    path('proddetails/<int:id>/',views.proddetails,name ='proddetails'),
    path('cartitems/',views.cartitems,name='cartitems'),
    path('removecart/<int:id>/',views.removecart,name='removecart'),
    path('buyitems/<int:id>/',views.buyitems,name='buyitems'),
    path('addDeliveryDetails/<int:id>/',views.addDeliveryDetails,name='addDeliveryDetails'),
    path('history/',views.history,name='history'),
    path('order/',views.order,name='order'),
    path('notification/',views.notification,name='notification'),
    path('buyerprofile/',views.buyerprofile,name='buyerprofile'),
    path('addressform/',views.addAddress,name='addAddress'),
    path('checkout/<int:id>/',views.checkout,name='checkout'),
    path('buyallproduct/',views.buyallproduct,name='buyallproduct'),
    path('checkoutallprod/',views.checkoutallprod,name='checkoutallprod'),
]
