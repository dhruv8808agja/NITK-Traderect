from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('product/<int:productID>/',views.product,name='product'),
    path('home/', views.index, name='index'),
    path('', views.login, name='login'),
]
