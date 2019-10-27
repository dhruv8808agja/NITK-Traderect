from django.shortcuts import render,get_object_or_404, redirect
from .models import *
import random
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required


@login_required()
def index(request):
    a=[[1,e.rentid,e.price,e.pid,e.pid.pname,e.pid.owner.name,e.pid.avgrating] for e in Rentad.objects.all()]
    for i in a:
            t=Photos.objects.select_related().filter(ownerid=i[3].pid)
            if t.exists():
                i.append('main_app/img/'+t.first().photofile.path.split('/')[-1])
            else:
                i.append('main_app/img/default.jpeg')
    b=[[0,e.sellid,e.price,e.pid,e.pid.pname,e.pid.owner.name] for e in Sellad.objects.all()]
    for i in b:
            a.append(i)
            t=Photos.objects.select_related().filter(ownerid=i[3].pid)
            if t.exists():
                i.append('main_app/img/'+t.first().photofile.path.split('/')[-1])
            else:
                i.append('main_app/img/default.jpeg')
    random.shuffle(a)
    return render(request, 'main_app/index.html', {'a':a})

def product(request, productID):
        product=get_object_or_404(Products, pk=productID)
        a=1
        b=1
        sellad=0
        rentad=0
        try:
            sellad=Sellad.objects.get(pk=product)
        except Sellad.DoesNotExist:
            a=0
        try:
            rentad=Rentad.objects.get(pk=product)
        except Rentad.DoesNotExist:
            b=0
        return render(request, 'main_app/product-page.html', {'product': product, 'sellad': sellad, 'rentad': rentad, 'a': a, 'b': b})

def login(request):
    if request.method=='GET':
        return render(request,'main_app/login.html')
    if request.method=='POST':
        user=authenticate(username=request.POST['email'],password=request.POST['password'])
        if user is not None:
            auth_login(request, user)
            return redirect('/home/')
        else:
            return render(request,'main_app/login.html')

def signup(request):
    if request.method=='GET':
        return render(request, 'main_app/signup.html')
    if request.method == 'POST':
        user = User.objects.create_user(request.POST['email'], request.POST['email'], request.POST['password'])
        user.save()
        u=Users.objects.create(email=request.POST['email'],name=request.POST['name'],phnumber=request.POST['phnumber'],whnumber=request.POST['whnumber'],address=request.POST['address'])
        u.save()
        return render(request, 'main_app/login.html')


def addNeed(request):
    if request.method == 'GET':
        return render(request, 'main_app/addNeed.html')
    if request.method == 'POST':
        user = Users.objects.filter(email=request.user)[0]
        need = Need.objects.create(productname=request.POST['productname'], description=request.POST['description'], category=request.POST['Category'], email=user)
        need.save()
        return redirect('/home/')


def allNeed(request):
    a = [[n.nid, n.productname, n.category] for n in Need.objects.all()]
    random.shuffle(a)
    return render(request, 'main_app/allNeed.html', {'a': a})


def addProduct(request):
    if request.method == 'GET':
        return render(request, 'main_app/addProduct.html')
    if request.method == 'POST':
        last_id = Products.objects.last()
        if last_id is None:
            last_id = 1
        else:
            last_id = last_id.pid + 1

        user = Users.objects.filter(email=request.user)[0]
        product = Products.objects.create(pid=last_id, pname=request.POST['pname'], category=request.POST['category'], description=request.POST['description'], owner=user)
        product.save()
        return redirect('/home/')


def myProducts(request):
    user = Users.objects.filter(email=request.user)[0]
    my_products = Products.objects.filter(owner=user)
    a = [[p.productname] for p in my_products]
    return render(request, 'main_app/myProducts.html', {'a': a})


