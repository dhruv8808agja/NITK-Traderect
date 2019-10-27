from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('product/<int:productID>/',views.product,name='product'),
    path('home/', views.index, name='index'),
    path('addNeed/', views.addNeed, name='addNeed'),
    path('allNeed/', views.allNeed, name='allNeed'),
    path('myProducts/', views.myProducts, name='myProducts'),
    path('addProduct/', views.addProduct, name='addProduct'),
    path('', views.login, name='login'),
]
