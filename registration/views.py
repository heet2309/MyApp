from django.http import HttpResponse,HttpResponseRedirect
from .models import RegistrationTable
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
import yagmail as mail
import random as rand

def registration_page(request):
    # if request.method == 'POST': 
    #     name = request.POST.get("name")
    #     email = request.POST.get("email")
    #     password = request.POST.get("password")
    #     phone = request.POST.get("phone")
        
    #     reg = RegistrationTable(name=name, email=email, password=password, phone=phone)
    #     reg.save()
            
            # Redirect to the OTP verification page on success
    
            

               
    return render(request, 'reg.html') 

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = RegistrationTable.Objects.get(email=email,password=password)
        
        
        if user:
            print("yes")
            return redirect('success')
        else:
            print("no")

    return render(request, 'login.html')


def welcome(request):
    return render (request,'welcome.html')

def success(request):
    return render (request,'success.html')

def home(request):
    return render (request,'home.html')
def contact(request):
    return render (request,'contact.html')

def products(request):
    return render (request,'products.html')

def about(request):
    return render (request,'about.html')

def authtication_otp(request):
    data="none"
   
    if request.method == "POST":
        otp = request.POST.get("otp_veri")
        email = request.POST.get("email_veri")
        print(otp)
        print(email)
        
        data = str(otp)+" "+str(email)
        #return HttpResponse(data)

    return HttpResponse(data)

def otp_var(request,email):
    

    return render(request,"otpver.html",{'email':email})
    
    
    
    
def verify(request):
    if request.method == 'POST': 
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")
        
        reg = RegistrationTable(name=name, email=email, password=password, phone=phone)
        reg.save()
        print("hello")
   
    try:
           
            rand_num = rand.randint(999, 10000)
            otp = f"{rand_num}"
            # with open("otp.html", "r") as file:
            #     html_content = file.read()

            #dynamic_html = html_content.replace( "<!-- Replace with dynamic OTP -->",f"<div class='otp'>{otp}</div>")
            smtp_server = mail.SMTP("heetlahute@gmail.com", "myuh ajbw mlzu qlvo")
            
            if request.method == 'POST':
                user_email = request.POST.get('email')
                with open("data.txt","w") as f:
                    f.write(str(user_email))
                
                #user = RegistrationTable.objects.get(email = email)
            smtp_server.send(
                to=user_email,
                subject="OTP Registration",
                contents=otp
            )

            print("Email sent successfully.")
            #request.session['user_email'] = user_email
            
            return  redirect(otp_var,email=str(user_email))

    except Exception as e:
            print(str(e))
            
            return HttpResponse(str(e))        

    #return render(request,'verify.html')
        
    
    
    
    
        
