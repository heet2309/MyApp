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
from registration.views import *

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', registration_page,name='reg'),
    path('login',login_view,name='login'),
    path('',welcome,name='welcome'),
    path('success',success,name='success'),
    path('home',home,name='home'),
    path('contact',contact,name='contact'),
    path('products',products,name='products'),
    path('about',about,name='about'),
    path('verifypage',verify,name='verifypage'),
    # path('otp_reg',otp_reg,name='otp_regis'),
    path('reset-password', PasswordResetView.as_view(), name='password_reset'), 
    path('reset-password/done', PasswordResetDoneView.as_view(), name='password_reset_done'), 
    path('reset-password/confirm/<uidb64>[0-9A-Za-z]+)-<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'), 
    path('reset-password/complete/',PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('otpver/<email>',otp_var,name="otp_verfication"),
    path('authtication_otp',authtication_otp,name="authtication_otp")
    


    
]
