from django.shortcuts import render ,redirect
from django.http import HttpResponse
from seller.models import Category , Products
from buyer.models import shoppcart
from django.contrib.auth.decorators import login_required
from ecommerce.models import UserProfile ,userAddress
from ecommerce.forms import userAddressForm
from django.contrib.auth.models import User
from ecommerce.models import userNotification ,buyerorder
from django.utils import timezone
import time

from django.contrib import auth



'''
from payu.gateway import get_hash
from uuid import uuid4
from payu.gateway import payu_url
from hashlib import sha512
'''
# Create your views here.

# @login_required
def buyerapp(request):
    count=0
    p=Products.objects.filter(product_avail__gt=0)
    
    for i in p:
        count+=1
    req='All'
    c=Category.objects.all()
    if request.method == 'POST' and request.POST['ser']:
        count=0
        req=request.POST['ser']
        p=Products.objects.filter(category__cat=req,product_avail__gt=0)
        for i in p:
            count+=1
    return render(request,'buyerproductpage.html',{'pro':p,'cat':c,'count':count,'req':req})

# @login_required
def proddetails(request,id):
    p=Products.objects.get(id=id)
    c=Category.objects.all()
    if request.method == 'POST':
        prod=Products.objects.get(id = id)
        try:
            cart = shoppcart(prodcartid = prod ,buyerid = request.user)
            cart.save()
        except Exception as e:
            pass
        return redirect('/cartitems/')
    return render(request,'viewproduct.html',{'pro':p,'cat':c})

@login_required
def cartitems(request):
    car = shoppcart.objects.filter(buyerid=request.user)
    c=Category.objects.all()
    total=0
    count=0
    for i in car:
        count+=1
        total = total + i.prodcartid.product_price
    return render(request,'showcart.html',{'cart':car,'total':total,'count':count,'cat':c})

@login_required
def removecart(request,id):
    obj=shoppcart.objects.get(id = id)
    obj.delete()
    return redirect('/buyer/cartitems/')

@login_required
def buyitems(request,id):
    #not used anymore
    return redirect('/buyer/cartitems/')

add = []
qty = 0
@login_required
def addDeliveryDetails(request,id):
    obj= UserProfile.objects.get(user__username = request.user.username)
    uobj = userAddress.objects.filter(uaddid = obj)
    have_add=False
    if uobj:
        have_add=True
        afrom = userAddressForm()
    else:
        afrom = userAddressForm()

    prod = shoppcart.objects.get(id = id)
    querryprod = prod.prodcartid
    if request.method == 'POST':
        global add
        address = request.POST.getlist('address')
        add = address
        global qty
        sel = request.POST.getlist('sel')
        qty = sel
        pay = request.POST.getlist('pay')
        try:
            total = 0
            total = int(sel[0]) * querryprod.product_price
        except Exception as e:
            pass
        if address == [] or sel == [] or pay == []:
            pass
        else:
            return render(request,'checkout.html',{'address':address[0],'quantaty':sel[0],'payment':pay[0],'product':querryprod,'total':total,'ide':id})
    context={'address':uobj,'product':querryprod,'idy':id,'afrom':afrom,'have_add':have_add}
    return render(request,'prodDeliveryDetails.html',context)

@login_required
def checkout(request,id):
    if request.method == 'POST':
        scartobj = shoppcart.objects.get(id = id)
        prodobj = Products.objects.get(id = scartobj.prodcartid.id)
        sellerid = prodobj.added_by_seller.id
        sellerobj = UserProfile.objects.get(id = sellerid)
        buyerobj = UserProfile.objects.get(user__id = request.user.id)
        now = timezone.now()
        temp = prodobj.product_avail - int(qty[0])
        if temp < 0:
            HttpResponse("<h4>Oopse ! Out of Stock</h4>")
            time.sleep(5)
            return redirect('/buyer/cartitems/')
        pobj = Products.objects.filter(id = prodobj.id)
        pobj.update(product_avail = temp)

        message = "Name:{},Product:{},Price:{},Quantity:{},Mobile:{},Address:{}".format(buyerobj.user.username,prodobj.product_name,prodobj.product_price,qty[0],buyerobj.mobile,add[0])
        obj = userNotification(userid = sellerobj , message = message, tim = now)
        obj.save()

        ob = buyerorder(userid = sellerobj,buyerid = request.user.id,productname=prodobj.product_name,productprice=prodobj.product_price,productqty=qty[0],buyermobile=buyerobj.mobile,buyeraddress=add[0],productimage=prodobj.product_img,status="ordered",tim=now)
        ob.save()
        #print(payu_url())
        return redirect('/buyer/order/')
    return render(request,'checkout.html')


@login_required
def history(request):
    return render(request,'history.html')

@login_required
def order(request):
    obj = buyerorder.objects.filter(buyerid = request.user.id).order_by('-tim')
    return render(request,'order.html',{'obj':obj})

@login_required
def notification(request):
    buyerobj = UserProfile.objects.get(user__id = request.user.id)
    obj = userNotification.objects.filter(userid = buyerobj).order_by('-tim')
    return render(request,'notification.html',{'notification':obj})

@login_required
def buyerprofile(request):
    obj= UserProfile.objects.get(user__username = request.user.username)
    uobj = userAddress.objects.filter(uaddid = obj)
    # print(uobj)
    mob=obj.mobile
    return render(request,'buyerprofile.html',{'mobile':mob,'obj':uobj})

@login_required
def addAddress(request):
    try:
        print(request.GET['next'])
        nex=True
        red=request.GET['next']

    except:
        nex=False
        print("False next")
        red='/buyer/buyerprofile/'

    obj= UserProfile.objects.get(user__username = request.user.username)
    uobj = userAddress.objects.filter(uaddid = obj)
    print(obj.user)
    afrom = userAddressForm()
    if request.method == 'POST':
        print('after posting',request.POST['red'])
        afrom = userAddressForm(request.POST)
        if afrom.is_valid():
            userAdd=afrom.save(commit=False)
            userAdd.uaddid=obj
            userAdd.save()
            if nex:
                return redirect(request.POST['red'])
            else:
                return redirect(request.POST['red'])

            # fo = userAddressForm(request.POST)
            # fo.save()

        else:
            afrom = userAddressForm()
            return render(request,'addressform.html',{'afrom':afrom})

        
    return render(request,'addressform.html',{'afrom':afrom,'red':red})


address=''
quantity=0
ids=0
payment=''
def buyallproduct(request):
    obj = shoppcart.objects.filter(buyerid = request.user.id)
    uobj = UserProfile.objects.get(user = request.user)
    aobj = userAddress.objects.filter(uaddid = uobj)
    if request.method == 'POST':
        global address , quantity , ids , payment
        address = request.POST.getlist('address')
        quantity = request.POST.getlist('selc')
        ids = request.POST.getlist('ide')
        payment = request.POST.getlist('pay')
        return redirect('/buyer/checkoutallprod/')
    return render(request,'buyallproduct.html',{'obj':obj,'address':aobj})

def checkoutallprod(request):
    global address , payment ,quantity
    dic = {}
    add = address
    pay = payment
    qty = list(map(int,quantity))
    obj = shoppcart.objects.filter(buyerid = request.user.id)
    j = 0
    total = 0
    for i in obj:
        total = total + i.prodcartid.product_price * qty[j]
        dic[i] = qty[j]
        j = j+1
    if request.method == 'POST':
        now = timezone.now()
        j = 0
        for i in obj:
            sellerobj = UserProfile.objects.get(id  = i.prodcartid.added_by_seller.id)
            prodobj = i.prodcartid
            buyerobj = UserProfile.objects.get(user__id = request.user.id)
            ob = buyerorder(userid = sellerobj,buyerid = request.user.id,productname=prodobj.product_name,productprice=prodobj.product_price,productqty=qty[j],buyermobile=buyerobj.mobile,buyeraddress=add[0],productimage=prodobj.product_img,status="ordered",tim=now)
            ob.save()
            j = j+1
        return redirect('/buyer/order/')
    return render(request,'checkoutallprod.html',{'product':dic,'address':add[0],'payment':pay[0],'total':total})
