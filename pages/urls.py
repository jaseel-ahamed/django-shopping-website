from django.urls import path
from . import views

from django.conf import settings

from django.conf.urls.static import static



urlpatterns=[
    path('',views.index,name='index'),
    path('registration',views.registration,name='registration'),
    path('login',views.login,name='login'),
    path('account',views.account,name='account'),
    path('logout',views.logout,name='logout'),
    path('addproduct',views.addproduct,name='addproduct'),
    path('products/<int:id>',views.viewproducts,name='products'),
    path('addtocart/<int:id>',views.addtocart,name='addtocart'),
    path('delcart/<int:id>',views.delcart,name='delcart'),
    path('delorder/<int:id>',views.delorder,name='delorder'),
    path('cart',views.cart,name='cart'),
    path('addtowish/<int:id>',views.addtowish,name='addtowish'),
    path('wishlist',views.wishlist,name='wishlist'),
    path('delwish/<int:id>',views.delwish,name='delwish'),
    path('checkout',views.checkout,name='checkout'),
    path('orders',views.orders,name='orders'),
    path('orderplaced',views.orderplaced,name='orderplaced'),
    path('purchase',views.purchase,name='purchase'),
    path('search',views.search,name='search'),

    #admin urls
    path('adminlogin',views.adminlogin,name='adminlogin'),
    path('adminproducts',views.adminproducts,name='adminproducts'),
    path('adminlogout',views.adminlogout,name='adminlogout'),
    path('admineditprod/<int:id>',views.admineditprod,name='admineditprod'),
    path('admindelprod/<int:id>',views.admindelprod,name='admindelprod'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)