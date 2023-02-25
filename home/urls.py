from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # //-- User URL's --//

    path('', views.landingpage, name='landingpage'),
    path('landingpage', views.landingpage, name='landingpage'),

    path('user_login', views.user_login, name='user_login'),
    path('login',views.login,name="login"),
    path('user_signup', views.user_signup, name='user_signup'),
    path('user_logout', views.user_logout, name='user_logout'),

    path('homepage', views.homepage, name='homepage'),
    path('userprofile', views.userprofile, name='userprofile'),

    path('cat_sort', views.cat_sort, name='cat_sort'),
    path('product_details', views.product_details, name='product_details'),
    path('productpage', views.productpage, name='productpage'),
    
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('cart', views.cart, name='cart'),
    path('cart_item_increment', views.cart_item_increment, name='cart_item_increment'),
    path('cart_item_decrement', views.cart_item_decrement, name='cart_item_decrement'),
    path('delete_cart_items', views.delete_cart_items, name='delete_cart_items'),
  
    path('otp_verification/<int:userid>/<str:secret>', views.otp_verification, name='otp_verification'),
    path('update_password', views.update_password, name='update_password'),
    path('update_email', views.update_email, name='update_email'),
    path('email_verification/<int:userid>/<str:secret>', views.email_verification, name='email_verification'),

    path('add_address', views.add_address, name='add_address'),
    path('checkout', views.checkout, name='checkout'),
    path('cash_on_delivery', views.cash_on_delivery, name='cash_on_delivery'),
    path('paypal', views.paypal, name='paypal'),

    path('user_order_cancel', views.user_order_cancel, name='user_order_cancel'),  
    path('order_history', views.order_history, name='order_history'),
    path('return_order', views.return_order, name='return_order'),
    path ('invoice', views.invoice, name='invoice'),

    # //-- Admin URL's --//

    path('admin_login',views.admin_login,name='admin_login'),
    path('admin_logout', views.admin_logout, name='admin_logout'),
    path('admin_home', views.admin_home,name='admin_home'),
    path ('salesreport', views.salesreport, name='salesreport'),

    path('user_management', views.user_management,name='user_management'),
    path('block_user', views.block_user,name='block_user'),
    path('unblock_user', views.unblock_user, name='unblock_user'),
    path('delete_user', views.delete_user, name='delete_user'),

    path('product_management', views.product_management, name='product_management'),
    path('delete_product', views.delete_product, name='delete_product'),
    path('update_product', views.update_product, name='update_product'),
    path('addproduct', views.addproduct, name='addproduct'),

    path('category_management', views.category_management, name='category_management'),
    path('addcategory', views.addcategory, name='addcategory'),
    path('update_category', views.update_category, name='update_category'),
    path('updatecategory', views.updatecategory, name='updatecategory'),
    path('delete_category', views.delete_category, name='delete_category'),

    path('order_management', views.order_management, name='order_management'),    
    path('cancel_order', views.cancel_order, name='cancel_order'),    
    path('order_details', views.order_details, name='order_details'),   
    path('status', views.status, name='status'),

    path('banner_management', views.banner_management, name='banner_management'),
    path('add_banner', views.add_banner, name='add_banner'),
    path('delete_banner', views.delete_banner, name='delete_banner'),  

    path('coupon_management', views.coupon_management, name='coupon_management'),
    path('addcoupon', views.addcoupon, name='addcoupon'),
    path('delete_coupon', views.delete_coupon, name='delete_coupon'),

    path('product_offer', views.product_offer, name='product_offer'),
    path('category_offer', views.category_offer, name='category_offer')
        
    

        
    ] +static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


