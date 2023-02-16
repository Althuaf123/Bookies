from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.landingpage, name='landingpage'),
    path('landingpage', views.landingpage, name='landingpage'),
    path('user_login', views.user_login, name='user_login'),
    path('login',views.login,name="login"),
    path('user_signup', views.user_signup, name='user_signup'),
    path('homepage', views.homepage, name='homepage'),
    path('userprofile', views.userprofile, name='userprofile'),
    path('product_details', views.product_details, name='product_details'),
    path('productpage', views.productpage, name='productpage'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('cart', views.cart, name='cart'),
    path('delete_cart_items', views.delete_cart_items, name='delete_cart_items'),
    path('add_address', views.add_address, name='add_address'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('admin_login',views.admin_login,name='admin_login'),
    path('admin_logout', views.admin_logout, name='admin_logout'),
    path('admin_home', views.admin_home,name='admin_home'),
    path('user_management', views.user_management,name='user_management'),
    path('block_user', views.block_user,name='block_user'),
    path('unblock_user', views.unblock_user, name='unblock_user'),
    path('delete_user', views.delete_user, name='delete_user'),
    path('product_management', views.product_management, name='product_management'),
    path('delete_product', views.delete_product, name='delete_product'),
    path('update_product', views.update_product, name='update_product'),
    path('updateproduct', views.updateproduct, name='updateproduct'),
    #path('add_product', views.add_product, name='add_product'),
    path('addproduct', views.addproduct, name='addproduct'),
    path('category_management', views.category_management, name='category_management'),
    path('addcategory', views.addcategory, name='addcategory'),
    path('update_category', views.update_category, name='update_category'),
    path('updatecategory', views.updatecategory, name='updatecategory'),
    path('delete_category', views.delete_category, name='delete_category'),
    path('order_management', views.order_management, name='order_management'),
    path('otp_verification/<int:userid>/<str:secret>', views.otp_verification, name='otp_verification'),
    path('checkout', views.checkout, name='checkout'),
    path('cash_on_delivery', views.cash_on_delivery, name='cash_on_delivery'),
    path('cancel_order', views.cancel_order, name='cancel_order'),
    path('user_order_cancel', views.user_order_cancel, name='user_order_cancel'),
    path('cart_item_increment', views.cart_item_increment, name='cart_item_increment'),
    path('cart_item_decrement', views.cart_item_decrement, name='cart_item_decrement'),
    # path('order_success', views.order_success, name='order_success'),
    path('order_history', views.order_history, name='order_history'),
    path('order_details', views.order_details, name='order_details'),
    path('update_password', views.update_password, name='update_password'),
    path('update_email', views.update_email, name='update_email'),
    path('email_verification/<int:userid>/<str:secret>', views.email_verification, name='email_verification'),
    # path('status_update', views.status_update, name='status_update'),
    path('update_phone', views.update_phone, name='update_phone'),
    path('status', views.status, name='status'),
    path('mobile_otp', views.mobile_otp, name='mobile_otp'),
    path('banner_management', views.banner_management, name='banner_management'),
    path('add_banner', views.add_banner, name='add_banner'),
    path('delete_banner', views.delete_banner, name='delete_banner'),
    path('paypal', views.paypal, name='paypal'),
    # path('cancell', views.cancell, name='cancell'),
    path('coupon_management', views.coupon_management, name='coupon_management'),
    path('addcoupon', views.addcoupon, name='addcoupon'),
    path('delete_coupon', views.delete_coupon, name='delete_coupon'),
    path('product_offer', views.product_offer, name='product_offer'),
    path('return_order', views.return_order, name='return_order'),

    


    
    
    ] +static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



