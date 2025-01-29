
from django.contrib import admin
from django.urls import path , include
from registration.views import *





urlpatterns = [
    path('admin/',admin.site.urls),
    path('',include('registration.urls')),
]




# from registration.views import registration_page,login_view,success,home,home_2,products,profile,contact,about,otp_var,update_profile,forgot_password,verify_otp,add_to_cart,buy_all_items,buy_item,remove_cart_item,cart_page,update_cart_quantity,order_summary,send_email_with_pdf,logout_view

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('reg', registration_page,name='reg'),
#     path('login',login_view,name='login'),
#     path('success/<int:id>/',success,name='success'),
#     path('',home,name='home'),
#     path('home2/<id>/',home_2,name='home2'),
#     path('profile/<int:id>/',profile, name='profile'),
#     path('update-profile',update_profile,name='update_profile'),
#     path('contact/<int:id>/',contact,name='contact'),
#     path('products',products,name='products'),
#     path('about/<int:id>/',about,name='about'),
#     path('otp-verification/<str:email>/', otp_var, name='otp_verification'),
#     path('forgot_password/', forgot_password, name='forgot_password'),
#     path('verify_otp/<str:email>/', verify_otp, name='verify_otp'),
#     path('add_to_cart/', add_to_cart, name='add_to_cart'),
#     path('cart/<int:user_id>/', cart_page, name='cart_page'),
    
#     path('remove_cart_item/', remove_cart_item, name='remove_cart_item'),
    
#     path('update_cart_quantity/', update_cart_quantity, name='update_cart_quantity'),
    
#     path('buy_item/', buy_item, name='buy_item'),
    
#     path('buy_all_items/', buy_all_items, name='buy_all_items'),
    
#     path('order_summary/<int:user_id>/', order_summary, name='order_summary'),
#     path('send_email_with_pdf/', send_email_with_pdf, name='send_email_with_pdf'),
#      path('logout/', logout_view, name='logout'),
# ]
   



    


# from django.contrib import admin
# from django.urls import path
# from registration.views import registration_page,login_view,success,home,home_2,products,profile,contact,about,otp_var,update_profile
# from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('reg', registration_page,name='reg'),
#     path('login',login_view,name='login'),
#     path('success',success,name='success'),
#     path('',home,name='home'),
#     path('home2/<id>/',home_2,name='home2'),
#     path('profile/<int:id>/',profile, name='profile'),
#     path('update_profile',update_profile,name='update_profile'),
#     path('contact',contact,name='contact'),
#     path('products',products,name='products'),
#     path('about',about,name='about'),
#     path('otp-verification/<str:email>/', otp_var, name='otp_verification'),
    
    # path('authtication_otp',authtication_otp,name="authtication_otp")
    
    # path('verifypage',verify,name='verifypage'),
    # path('otp_reg',otp_reg,name='otp_regis'),
    # path('reset-password', PasswordResetView.as_view(), name='password_reset'), 
    # path('reset-password/done', PasswordResetDoneView.as_view(), name='password_reset_done'), 
    # path('reset-password/confirm/<uidb64>[0-9A-Za-z]+)-<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'), 
    # path('reset-password/complete/',PasswordResetCompleteView.as_view(),name='password_reset_complete'),    

