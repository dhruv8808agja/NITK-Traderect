from django.urls import path

from . import views

urlpatterns = [
    path('product/<int:productID>/',views.product,name='product'),
    path('', views.index, name='index'),
]
