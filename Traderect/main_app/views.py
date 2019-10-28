from django.shortcuts import render,get_object_or_404, redirect
from .models import *
import random
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db import IntegrityError
from .forms import 
from operator import itemgetter

@login_required()
def index(request):
    # a=[[1,e.rentid,e.price,e.pid,e.pid.pname,e.pid.owner.name,e.pid.avgrating] for e in Rentad.objects.all()]
    # for i in a:
    #         t=Photos.objects.select_related().filter(ownerid=i[3].pid)
    #         if t.exists():
    #             i.append('main_app/img/'+t.first().photofile.path.split('/')[-1])
    #         else:
    #             i.append('main_app/img/default.jpeg')
    # b=[[0,e.sellid,e.price,e.pid,e.pid.pname,e.pid.owner.name] for e in Sellad.objects.all()]
    # for i in b:
    #         a.append(i)
    #         t=Photos.objects.select_related().filter(ownerid=i[3].pid)
    #         if t.exists():
    #             i.append('main_app/img/'+t.first().photofile.path.split('/')[-1])
    #         else:
    #             i.append('main_app/img/default.jpeg')
    # random.shuffle(a)
    categoryID = 0
    sortID = 0
    return home_category_sort(request, categoryID, sortID)
    # return render(request, 'main_app/index.html', {'a': a})


def home_category_sort(request, categoryID, sortID):
    #make this variables global to project like cat1, cat2
    user = Users.objects.filter(email=request.user)[0]

    if categoryID == 0:
        mycategory = 'all'
    elif categoryID == 1:
        mycategory = 'electronics'
    elif categoryID == 2:
        mycategory = 'stationary'
    elif categoryID == 3:
        mycategory = 'vehicles'
    else:
        mycategory = 'others'

    if categoryID == 0:
        print('in first')
        this_cat_products = Products.objects.all().exclude(owner=user) #not handled for null
    else:
        print('in second')
        this_cat_products = Products.objects.filter(category=mycategory).exclude(owner=user)

    print(this_cat_products)
    # reference_products = [[p.pid, p.pname, p.category, p.description, p.owner.name, p.avgrating]
    #                       for p in this_cat_products]
    a=[]
    b=[]
    for element in this_cat_products:
        try:
            e=Rentad.objects.get(pk=element)
            a.append([1, e.rentid, e.price, e.pid.pid, e.pid.pname, e.pid.owner.name, e.pid.avgrating])
        except Rentad.DoesNotExist:
            pass
    print("its A: ", a)

    # for i in a:
    #     t = Photos.objects.select_related().filter(ownerid=i[3].pid)
    #     if t.exists():
    #         i.append('main_app/img/' + t.first().photofile.path.split('/')[-1])
    #     else:
    #         i.append('main_app/img/defendforault.jpeg')

    for element in this_cat_products:
        try:
            ins=Sellad.objects.get(pk=element)
            b.append([0,ins.sellid,ins.price,ins.pid.pid,ins.pid.pname,ins.pid.owner.name])
        except:
            pass
    print("its B: ", b)
    # for i in b:
    #     a.append(i)
    #     t = Photos.objects.select_related().filter(ownerid=i[3].pid)
    #     if t.exists():
    #         i.append('main_app/img/' + t.first().photofile.path.split('/')[-1])
    #     else:
    #         i.append('main_app/img/default.jpeg')
    for i in b:
        a.append(i)
    wow_a = a
    print("ITS ALL A: ", a)
    if sortID == 0:
        print('SORT 0')
        random.shuffle(wow_a)
    elif sortID == 1:
        print('SORT 1')
        wow_a = sorted(a, key=lambda x: x[2])
    else:
        print('SORT 2')
        wow_a = sorted(a, key=lambda x: x[2], reverse=True)
    print("ALL A SORTED: ", a)


    return render(request, 'main_app/index.html', {'a': wow_a, 'sortID': sortID, 'categoryID': categoryID})


def search_post(request):
    user = Users.objects.filter(email=request.user)[0]
    if request.POST['search'] == '':
        return redirect('/home/0/0')
    else:
        a = []
        b = []
        product_matched_l = []
        search_str = request.POST['search']
        all_product_q = Products.objects.all().exclude(owner=user)
        for element in all_product_q:
            if search_str in element.pname:
                product_matched_l.append(element)

         # product_matched_q = Products.objects.filter(pname=request.POST['search'])
        if len(product_matched_l) == 0:
            return render(request, 'main_app/index.html', {'a': [], 'sortID': request.POST['sortID'], 'categoryID': request.POST['categoryID']})
        else:
            for element in product_matched_l:
                try:
                    e = Rentad.objects.get(pk=element)
                    a.append([1, e.rentid, e.price, e.pid.pid, e.pid.pname, e.pid.owner.name, e.pid.avgrating])
                except Rentad.DoesNotExist:
                    pass

            for element in product_matched_l:
                try:
                    ins = Sellad.objects.get(pk=element)
                    b.append([0, ins.sellid, ins.price, ins.pid.pid, ins.pid.pname, ins.pid.owner.name])
                except:
                    pass

            for i in b:
                a.append(i)
            return render(request, 'main_app/index.html', {'a': a})



#redirect('/home/' + request.POST['categoryID'] + '/' + request.POST['sortID'] + '/')


def product(request, productID):
        product=get_object_or_404(Products, pk=productID)
        a=1
        b=1
        sellad=0
        rentad=0
        flag=0
        t=1
        try:
            sellad=Sellad.objects.get(pk=product)
        except Sellad.DoesNotExist:
            a=0
        try:
            rentad=Rentad.objects.get(pk=product)
            t=[[str(i.startdate)+" "+str(i.starttime),str(i.enddate)+" "+str(i.endtime)] for i in Renttransaction.objects.select_related().filter(rentid=rentad)]
            if len(t)!=0:
                flag=1
            print(flag)
        except Rentad.DoesNotExist:
            b=0

        #for wish list
        user = Users.objects.filter(email=request.user)[0]
        my_products = Products.objects.filter(owner=user)[0]
        wishes = Wishes.objects.filter(email=user, pid=my_products)
        wished = 0
        if wishes.exists():
            wished = 1

        print(wished)
        return render(request, 'main_app/product-page.html', {'product': product, 'sellad': sellad, 'rentad': rentad, 'a': a, 'b': b,'t':t,'flag':flag, 'wished': wished})


def login(request):
    if request.method=='GET':
        return render(request,'main_app/login.html')
    if request.method=='POST':
        user=authenticate(username=request.POST['email'],password=request.POST['password'])
        if user is not None:
            auth_login(request, user)
            return redirect('/home/')
        else:
            return render(request, 'main_app/login.html')


def logout(request):
    auth_logout(request)
    return redirect('/')


def signup(request):
    if request.method=='GET':
        return render(request, 'main_app/signup.html')
    if request.method == 'POST':
        user = User.objects.create_user(request.POST['email'], request.POST['email'], request.POST['password'])
        user.save()
        u=Users.objects.create(email=request.POST['email'],name=request.POST['name'],phnumber=request.POST['phnumber'],whnumber=request.POST['whnumber'],address=request.POST['address'])
        u.save()
        return render(request, 'main_app/login.html')


@login_required
def addNeed(request):
    if request.method == 'GET':
        return render(request, 'main_app/addNeed.html')
    if request.method=='POST':
        print(request.POST)
        print(request.FILES)
        user = Users.objects.filter(email=request.user)[0]
        need = Need.objects.create(productname=request.POST['productname'], description=request.POST['description'], category=request.POST['Category'], email=user)
        need.save()
        return redirect('/myNeed/')


def allNeed(request):
    a = [[n.nid, n.productname, n.category] for n in Need.objects.all() if n.email.email!=request.user.email]
    random.shuffle(a)
    return render(request, 'main_app/allNeed.html', {'a': a})


def myNeed(request):
    a = [[n.nid, n.productname, n.category] for n in Need.objects.all() if n.email.email==request.user.email]
    return render(request, 'main_app/myNeeds.html', {'a': a})


def editNeed(request, needID):
    if request.method == 'GET':
        this_need = Need.objects.filter(nid=needID)[0]
        return render(request, 'main_app/editNeed.html', {'need': this_need})


def editNeed_post(request):
    this_need = Need.objects.filter(nid=request.POST['nid'])[0]
    this_need.productname = request.POST['productname']
    this_need.description = request.POST['description']
    this_need.category = request.POST['category']
    this_need.save()
    return redirect('/myNeed/')


def addProduct(request):
    if request.method == 'GET':
        last_id = Products.objects.last()
        if last_id is None:
            last_id = 1
        else:
            last_id = last_id.pid + 1
        last_id_1 = Photos.objects.last()
        if last_id_1 is None:
            last_id_1 = 1
        else:
            last_id_1 = last_id_1.photoid + 1
        form = PhotoForm(initial={'photoid':last_id_1,'ownerid':last_id})
        form.fields['photoid'].widget = forms.HiddenInput()
        form.fields['ownerid'].widget = forms.HiddenInput()
        return render(request, 'main_app/addProduct.html',{'form':form})
    if request.method == 'POST':
        last_id = Products.objects.last()
        if last_id is None:
            last_id = 1
        else:
            last_id = last_id.pid + 1
        print(request.FILES)
        print(type(request.FILES.get('myFile')))
        print(dir(request.FILES.get('myFile')))
        #request.POST['ownerid']=last_id
        last_id_1 = Photos.objects.last()
        if last_id_1 is None:
            last_id_1 = 1
        else:
            last_id_1 = last_id_1.photoid + 1
        #request.POST['photoid']=last_id_1
        form=PhotoForm(request.POST,request.FILES,{'ownerid':last_id,'photoid':last_id_1})
        if form.is_valid():
            form.save()
        else:
            print("ERROR IS THERE")
            form.fields['photoid'].widget = forms.HiddenInput()
            form.fields['ownerid'].widget = forms.HiddenInput()
            return render(request, 'main_app/addProduct.html', {'form': form})
        user = Users.objects.filter(email=request.user)[0]
        product = Products.objects.create(pid=last_id, pname=request.POST['pname'], category=request.POST['category'], description=request.POST['description'], owner=user)
        product.save()
        return redirect('/myProducts/')


def wishlist(request):
    user = Users.objects.filter(email=request.user)[0]
    my_wishes = Wishes.objects.filter(email=user)
    print(my_wishes)
    my_wished_products = []
    for element in my_wishes:
        my_wished_products.append(element)

    #print(my_wished_products[0].pid)
    return render(request, 'main_app/wishlist.html', {'products': my_wished_products})



def myProducts(request):
    if request.method == 'GET':
        user = Users.objects.filter(email=request.user)[0]
        my_products = Products.objects.filter(owner=user)
        a = [[p.pid, p.pname] for p in my_products]
        for i in a:
            try:
                ins= Rentad.objects.get(pk=i[0])
                i.append(1)
            except Rentad.DoesNotExist:
                i.append(0)
        return render(request, 'main_app/myProducts.html', {'a': a})


def product_page(request, productID):
    product = get_object_or_404(Products, pk=productID)
    a = 1
    b = 1
    sellad = 0
    rentad = 0
    flag = 0
    t = 1
    try:
        sellad = Sellad.objects.get(pk=product)
    except Sellad.DoesNotExist:
        a = 0
    try:
        rentad = Rentad.objects.get(pk=product)
        t = [[str(i.startdate) + " " + str(i.starttime), str(i.enddate) + " " + str(i.endtime)] for i in
             Renttransaction.objects.select_related().filter(rentid=rentad)]
        if len(t) != 0:
            flag = 1
        print(flag)
    except Rentad.DoesNotExist:
        b = 0
    return render(request, 'main_app/product-page1.html', {'product': product, 'sellad': sellad, 'rentad': rentad, 'a': a, 'b': b,'t':t,'flag':flag})


def product_delete(request, productID):
    instance = Products.objects.get(pk=productID)
    instance.delete()
    return redirect('/myProducts/')


def edit_product_page(request, productID):
    if request.method == 'GET':
        this_product = Products.objects.filter(pid=productID)[0]
        return render(request, 'main_app/editProduct.html', {'product': this_product})


def edit_product_page_post(request):
    print(request.POST)
    this_product = Products.objects.get(pk=request.POST['pid'])
    this_product.pname = request.POST['pname']
    this_product.description = request.POST['description']
    this_product.category = request.POST['category']
    print(this_product.pid)
    check_var=1
    #checks handling
    try:
        check_var = request.POST.getlist('checks[]')[0]
        print(check_var)
    except IndexError:
        rentadinstance=Rentad.objects.filter(pid=this_product.pid)
        try:
            a=rentadinstance[0]
            a.delete()
        except IndexError:
            pass
        selladinstance=Sellad.objects.filter(pid=this_product.pid)
        try:
            a=selladinstance[0]
            a.delete()
        except IndexError:
            pass
        return redirect('/myProducts/')

    if '1' in check_var:
        selladinstance = Sellad.objects.filter(pk=this_product.pid)
        if selladinstance.exists() == False:
            last_id = Sellad.objects.last()
            if last_id is None:
                last_id = 1
            else:
                last_id = last_id.pid.pid + 1

            selladinstance = Sellad.objects.create(sellid=last_id, pid=this_product,
                                                   price=request.POST['sell_price'],
                                                   adddate=datetime.date(datetime.now()),
                                                   expirydate=request.POST['sell_expDate'])
            selladinstance.save()
        else:
            selladinstance2 = Sellad.objects.get(pk=this_product.pid)
            selladinstance2.price = request.POST['sell_price']
            selladinstance2.expirydate = request.POST['sell_expDate']
            selladinstance2.save()

        if '2' not in check_var:
            rentadinstance = Rentad.objects.filter(pk=this_product.pid)
            if rentadinstance.exists():
                rentadinstance[0].delete()

    if '2' in check_var:
        rentadinstance = Rentad.objects.filter(pk=this_product.pid)
        if rentadinstance.exists() == False:
            last_id = Rentad.objects.last()
            if last_id is None:
                last_id = 1
            else:
                last_id = last_id.pid.pid + 1

            rentadinstance = Rentad.objects.create(rentid=last_id, pid=this_product, price=request.POST['rent_price'], description=request.POST['rent_description'],
                                                   adddate=datetime.date(datetime.now()),
                                                   expirydate=request.POST['rent_expDate'])
            rentadinstance.save()
        else:
            rentadinstance2 = Rentad.objects.get(pk=this_product.pid)
            rentadinstance2.price = request.POST['rent_price']
            rentadinstance2.expirydate = request.POST['rent_expDate']
            rentadinstance2.description = request.POST['rent_description']
            rentadinstance2.save()

        if '1' not in check_var:
            selladinstance = Sellad.objects.filter(pk=this_product.pid)
            if selladinstance.exists():
                selladinstance[0].delete()
    this_product.save()
    return redirect('/myProducts/')


def needDetail(request,nid):
    need=get_object_or_404(Need, pk=nid)
    return render(request, 'main_app/needDetails.html', {'need': need})

def deleteNeed(request,nid):
    instance = Need.objects.get(pk=nid)
    instance.delete()
    return redirect('/myNeed/')

def new_rent(request,productID):
    rentad = Rentad.objects.filter(pid=productID)[0]
    product= Products.objects.get(pk=productID)
    return render(request,'main_app/new_rent.html',{'rentad':rentad,'product':product})


def new_rent_post(request):
    print(request.POST)
    str=request.POST['pid']+"+"+request.POST['startDate']+"+"+request.POST['startTime']+"+"+request.POST['endDate']+"+"+request.POST['endTime'];
    inst=Renttransaction.objects.create(rentid=Rentad.objects.get(pk=request.POST['pid']),email=Users.objects.get(pk=request.POST['email']),startdate=request.POST['startDate'],starttime=request.POST['startTime'],enddate=request.POST['endDate'],endtime=request.POST['endTime'])
    return redirect('/home')


def addToWish(request, productID):
    user = Users.objects.filter(email=request.user)[0]
    my_product = Products.objects.filter(pid=productID)[0]
    print(my_product)
    wishlist1 = Wishes.objects.create(email=user, pid=my_product)

    try:
        wishlist1.save()
    except IntegrityError:
        pass
    return redirect('/product/' + str(productID))


def deleteWish(request, productID):
    product_o = Products.objects.get(pk = productID)
    wish_o = Wishes.objects.filter(pid = product_o)
    wish_o.delete()
    return redirect('/wishlist/')
