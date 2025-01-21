"""
URL configuration for demoreg project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from registration.views import registration_page,login_view,success,home,home_2,products,profile,contact,about,otp_var,update_profile,forgot_password,verify_otp,add_to_cart,cart,RemoveFromCartView,ReduceQuantityView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reg', registration_page,name='reg'),
    path('login',login_view,name='login'),
    path('success/<int:id>/',success,name='success'),
    path('',home,name='home'),
    path('home2/<id>/',home_2,name='home2'),
    path('profile/<int:id>/',profile, name='profile'),
    path('update-profile',update_profile,name='update_profile'),
    path('contact/<int:id>/',contact,name='contact'),
    path('products',products,name='products'),
    path('about/<int:id>/',about,name='about'),
    path('otp-verification/<str:email>/', otp_var, name='otp_verification'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('verify_otp/<str:email>/', verify_otp, name='verify_otp'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('cart/<int:user_id>/', cart, name='cart'),
    path('remove_from_cart_api/', RemoveFromCartView, name='remove_from_cart_api'),
    path('reduce_quantity_api/', ReduceQuantityView, name='reduce_quantity_api'),

]

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

