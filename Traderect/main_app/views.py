from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.
def index(request):
    a=[[1,e.rentid,e.price,e.pid,e.pid.pname,e.pid.owner.name] for e in Rentad.objects.all()]
    print("Output || ",a)
    p={}
    for i in a:
            t=Photos.objects.select_related().filter(ownerid=i[3].pid)
            if t.exists():
                print(t.first())
                p[i[3].pid]=t.first().photofile
            else:
                p[i[3].pid]='main_app/img/traderect.png'
    context={'a':a,'p':p}
    return render(request, 'main_app/index.html',context)
