from django.urls import path
from .views import *



urlpatterns = [
    path('reg', registration_page, name='reg'),
    path('login', login_view, name='login'),
    path('success/<int:id>/', success, name='success'),
    path('', home, name='home'),
    path('home2/<int:id>/', home_2, name='home2'),
    path('profile/<int:id>/', profile, name='profile'),
    path('update-profile', update_profile, name='update_profile'),
    path('contact/<int:id>/', contact, name='contact'),
    path('products', products, name='products'),
    path('about/<int:id>/', about, name='about'),
    path('otp-verification/<str:email>/', otp_var, name='otp_verification'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('verify_otp/<str:email>/', verify_otp, name='verify_otp'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('cart/<int:user_id>/', cart_page, name='cart_page'),
    path('remove_cart_item/', remove_cart_item, name='remove_cart_item'),
    path('update_cart_quantity/', update_cart_quantity, name='update_cart_quantity'),
    path('buy_item/', buy_item, name='buy_item'),
    path('buy_all_items/', buy_all_items, name='buy_all_items'),
    path('order_summary/<int:user_id>/', order_summary, name='order_summary'),
    path('send_email_with_pdf/', send_email_with_pdf, name='send_email_with_pdf'),
    path('logout/', logout_view, name='logout'),
    path('home_edit/', home_edit, name='home_edit'),
    path('home2edit/', home2edit, name='home2edit'),
    path('DashBoard', DashBoard, name='DashBoard')
]