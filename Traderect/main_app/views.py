from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import random
# Create your views here.
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
    return render(request, 'main_app/index.html',{'a':a,})
