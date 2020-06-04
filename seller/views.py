from django.shortcuts import render , redirect
from django.http import HttpResponse
from seller.forms import sellerform
from seller.models import Category , Products
from django.contrib.auth.decorators import login_required
from ecommerce.models import UserProfile , userNotification ,buyerorder
from django.utils import timezone

# Create your views here.
@login_required
def sellerapp(request):
    return render(request,'sellerpage.html')

@login_required
def addproduct(request):
    lis=Category.objects.all()
    if request.method == 'POST':
        name = request.POST['pname']
        desc = request.POST['desc']
        price = request.POST['price']
        sellby = UserProfile.objects.get(user__username=request.user)
        img = request.FILES['fil']
        avail = request.POST['qty']
        cat = Category.objects.get(cat=request.POST['catid'])
        savdat = request.POST['sav']
        moddat = request.POST['mod']
        s=Products(product_name=name,product_desc=desc,product_price=price,added_by_seller=sellby,product_img=img,product_avail=avail,category=cat,saveDate=savdat,modifiedDate=moddat)
        s.save()
        return redirect('/seller/addproduct/')
    else:
        return render(request,'addproduct.html',{'lis':lis})
@login_required
def addcategory(request):
    lis=Category.objects.all()
    if request.method == 'POST':
        cat = request.POST['ncat']
        c = Category(cat=cat)
        c.save()
        return redirect('/seller/addcategory/')
    return render(request,'addcategory.html',{'lis':lis})

@login_required
def addedproduct(request):
    p = Products.objects.filter(added_by_seller__user__username=request.user)
    return render(request,'addedproduct.html',{'prod':p})

@login_required
def modifyproduct(request,id):
    obj = Products.objects.get(id = id)
    if request.method == 'POST':
        name = request.POST['pname']
        desc = request.POST['desc']
        price = request.POST['price']
        avail = request.POST['qty']
        moddat = request.POST['mod']
        ob = Products.objects.filter(id = id)
        ob.update(product_name=name,product_desc=desc,product_price=price,product_avail=avail,modifiedDate=moddat)
        return redirect('/seller/addedproduct/')
    return render(request,'modifyproduct.html',{'obj':obj})

@login_required
def sellernotifications(request):
    sellerobj = UserProfile.objects.get(user__id = request.user.id)
    obj = userNotification.objects.filter(userid = sellerobj).order_by('-tim')
    return render(request,'sellernotifications.html',{'obj':obj})

@login_required
def createnotifications(request):
    if request.method == 'POST':
        message = request.POST.getlist('tname')
        mess = message[0]
        obj = UserProfile.objects.all()
        now = timezone.now()
        for i in obj:
            if i.usertype == 'buyer':
                ob = userNotification(userid = i , message = mess ,tim = now)
                ob.save()
    return render(request,'createnotification.html')

@login_required
def sellerorders(request):
    uobj = UserProfile.objects.get(user = request.user)
    obj = buyerorder.objects.filter(userid = uobj).order_by('-tim')
    return render(request,'sellerorders.html',{'obj':obj})

@login_required
def sellershippcall(request,id):
    obj = buyerorder.objects.filter(id = id)
    shipp = 'shipped at '+ str(timezone.now())
    obj.update(status=shipp)
    return redirect('/seller/sellerorders/')
