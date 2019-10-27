from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('product/<int:productID>/',views.product,name='product'),
    path('home/', views.index, name='index'),
    path('addNeed/', views.addNeed, name='addNeed'),
    path('editNeed/<int:needID>/', views.editNeed, name='editNeed'),
    path('editNeed/post/', views.editNeed_post, name='editNeed_post'),
    path('needDetail/<int:nid>/', views.needDetail, name='needDetail'),
    path('allNeed/', views.allNeed, name='allNeed'),
    path('myNeed/', views.myNeed, name='myNeed'),
    path('deleteNeed/<int:nid>/', views.deleteNeed, name='deleteNeed'),
    path('addProduct/', views.addProduct, name='addProduct'),
    path('myProducts/', views.myProducts, name='myProducts'),
    path('product-page/<int:productID>/', views.product_page, name='product_page'),
    path('product_delete/<int:productID>/', views.product_delete, name='product_delete'),
    path('new_rent/<int:productID>/', views.new_rent, name='new_rent'),
    path('new_rent_post/', views.new_rent_post, name='new_rent_post'),
    path('edit_product_page/<int:productID>/', views.edit_product_page, name='edit_product_page'),
    path('edit_product_page/post/$/', views.edit_product_page_post, name='edit_product_page_post'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('addToWish/<int:productID>/', views.addToWish, name='addToWish'),
    path('', views.login, name='login'),
]
