from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import TemporaryTable, RegistrationTable,Product,Cart
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import yagmail as mail
import random as rand
from django.contrib.auth.models import User
import json
import logging
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

def registration_page(request):
    if request.method == 'POST':

        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")
        
       
        otp = rand.randint(1000, 9999)

        try:
            smtp_server = mail.SMTP(
                "heetlahute@gmail.com", "myuh ajbw mlzu qlvo")
            smtp_server.send(
                to=email,
                subject="OTP Verification",
                contents=f"your OTP is {otp}"
            )
            print("Email Sent Successfulyy")

            temp_reg = TemporaryTable(
            name=name, phone=phone, email=email, otp=otp, password=password)
            temp_reg.save()

        except Exception as e:
            print(str(e))
            return HttpResponse(str(e))
        return redirect(otp_var, email=str(email))

    return render(request, 'reg.html')


def login_view(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = RegistrationTable.objects.get(email=email, password=password)

        if user:
            print("yes")
            return redirect(home_2, id=user.id)
        else:
            print("no")

    return render(request, 'login.html')


def success(request,id):
    
    user = RegistrationTable.objects.get(id=id)
    data = {
        'id': id
    }
    return render(request, 'success.html',{'user': data})


def profile(request, id):

    try:
        user = RegistrationTable.objects.get(id=id)
        data = {
            'name': user.name,
            'email': user.email,
            'phone': user.phone,
            'id': user.id
        }
    except RegistrationTable.DoesNotExist:
        return HttpResponse("User not found")

    return render(request, 'profile.html', {'user': data})


logger = logging.getLogger(__name__)


@csrf_exempt
def update_profile(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            name = data.get('name')
            email = data.get('email')
            phone = data.get('phone')

            logger.debug(f"Received data: {data}")

            # user= RegistrationTable.objects.get(id=user.id)

            user = get_object_or_404(RegistrationTable, id=user_id)
            user.name = name
            user.email = email
            user.phone = phone
            user.save()

            return JsonResponse({'success': True, 'message': 'Profile updated successfully.'})
        except Exception as e:
            logger.error(f"Error updating profile: {str(e)}")
            return JsonResponse({'success': False, 'message': 'Error updating profile.'})
    return JsonResponse({'success': False, 'message': 'Invalid request.'})



def home(request):
    return render(request, 'home.html')



def home_2(request, id):

    data = {
        'id': id
    }

    return render(request, "home2.html", {'data': data})


def contact(request, id):

    data = {
        'id': id
    }
    return render(request, 'contact.html', {'data': data})

def products(request):
    products_list = Product.objects.all()
    paginator = Paginator(products_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user_id = None
    if request.user.is_authenticated:
        try:
            registration = RegistrationTable.objects.get(user=request.user)
            user_id = registration.user.id
        except RegistrationTable.DoesNotExist:
            user_id = None

    context = {
        "page_obj": page_obj,
        "user_id": user_id
    }
    return render(request, "products.html", context)

# def products(request):
    
#     products_list = Product.objects.all()
#     paginator = Paginator(products_list,3)  
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     context = {
#         "page_obj": page_obj,
#         "user_id": request.user.id if request.user.is_authenticated else None
#     }
#     return render(request, "products.html", context)
# def products(request):

#     products = Product.objects.all()
#     return render(request, "products.html", {"products": products})

   
  
    # products = Product.objects.all() 

    # with open('pro.txt' ,"a") as f:
    #     for products in products:
    #         f.write(str(products))
            
    # return render(request, 'products.html', {'data': data})




def about(request, id):

    data = {
        'id': id
    }
    return render(request, 'about.html', {'data': data})

def otp_var(request, email):
    if request.method == 'POST':
        otp1 = request.POST.get("o1")
        otp2 = request.POST.get("o2")
        otp3 = request.POST.get("o3")
        otp4 = request.POST.get("o4")

        final_otp = str(otp1) + str(otp2) + str(otp3) + str(otp4)

        try:
            temp_reg = TemporaryTable.objects.get(email=email, otp=final_otp)

            reg = RegistrationTable(
                name=temp_reg.name,
                email=temp_reg.email,
                phone=temp_reg.phone,
                password=temp_reg.password
            )
            reg.save()

            # Clean up temporary registration entry
            temp_reg.delete()

            # Redirect to success.html
            return redirect('success')  # 'success' should be a valid URL pattern name
        except TemporaryTable.DoesNotExist:
            messages.error(request, "Invalid OTP or expired OTP. Please try again.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    # Render the OTP verification page
    return render(request, 'otpver.html', {'email': email})


def sendmail(request, email):
    try:

        server = mail.SMTP("heetlahute@gmail.com", "myuh ajbw mlzu qlvo")
        server.send(
            to=email,
            subject="Registration Successful",
            contents=r"D:\demoreg\templates\sendmail.html"
        )
    except Exception as e:
        print("Fail to send confirmation email")


# Store OTPs temporarily
otp_storage = {}


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = RegistrationTable.objects.get(email=email)
            otp = rand.randint(1000, 9999)
            otp_storage[email] = otp

            # Send OTP using yagmail
            yag = mail.SMTP("heetlahute@gmail.com", "myuh ajbw mlzu qlvo")
            yag.send(
                to=email,
                subject="Password Reset OTP",
                contents=f"Your OTP for password reset is: {
                    otp}. It is valid for 10 minutes."
            )
            messages.success(
                request, "OTP sent to your email. Please check your inbox.")
            return redirect('verify_otp', email=email)
        except RegistrationTable.DoesNotExist:
            messages.error(request, "Email does not exist.")
    return render(request, 'forgot_password.html')

def verify_otp(request, email):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')


        if email in otp_storage and otp_storage[email] == int(otp):
            user = RegistrationTable.objects.get(email=email)
            user.password = new_password
            user.save()
            del otp_storage[email]  # Clear OTP after use
            messages.success(request, "Password reset successfully. Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP or expired.")
    return render(request, 'verify_otp.html', {'email': email})

class AddToCartView():
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user_id = data.get('user_id')
        product_id = data.get('product_id')
        quantity = data.get('quantity')

        try:
            product = Product.objects.get(id=product_id)
            cart_item, created = Cart.objects.get_or_create(user_id=user_id, product=product)

            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity

            cart_item.save()
            return JsonResponse({'success': True, 'message': 'Item added to cart.'})
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
# # @login_required
# @csrf_exempt
# def update_profile(request):
#     if request.method == 'POST':
#         try:
#             # Parse JSON data
#             data = json.loads(request.body)
#             user_id = data.get('user_id')
#             name = data.get('name')
#             email = data.get('email')
#             phone = data.get('phone')

#             user = get_list_or_404(RegistrationTable, id=user.id)
#             user.name = name
#             user.email = email
#             user.phone = phone
#             user.save()

#             return JsonResponse({'success': True, 'messages': 'Profile updated successfully!!'})
#         except Exception as e:
#             return JsonResponse({'success': False, 'messages': str(e)})
#     return JsonResponse ({'success':False, 'message':'Invalid Request'})


    # if request.method  == "POST":
    #     data = json.loads(request.body)

    #     email = data.get("email")
    #     password = data.get("password")

    #     user = RegistrationTable.objects.get(email=email, password=password)

    #     response_data = {
    #         'id': user.id,
    #     }

    #     return JsonResponse(response_data)
    # return JsonResponse({'status': 405, 'message': 'Method not allowed'})

    # if request.method == "POST":
    #     data = json.loads(request.body)

    #     email = data.get("email")
    #     password = data.get("password")

    #     user = RegistrationTable.objects.get(
    #         email=email, password=password)

    #     response_data = {
    #         'id': user.id,
    #     }

    #     return JsonResponse(response_data)
    # return JsonResponse({'status': 405, 'message': 'Method not allowed'})

# def forgot_password(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')

#         try:
#             user = RegistrationTable.objects.get(email=email)
#         except RegistrationTable.DoesNotExist:
#             messages.error(request, 'Email not found.')
#             return redirect('forgot_password')

#         otp = rand.randint(1000, 9999)

#         try:
#             smtp_server = mail.SMTP("heetlahute@gmail.com",  "myuh ajbw mlzu qlvo")
#             smtp_server.send(
#                 to=email,
#                 subject="OTP Verification",
#                 contents=f"Your OTP is {otp}"
#             )
#             print("Email Sent Successfully")

#             temp_reg = TemporaryTable(email=email, otp=otp)
#             temp_reg.save()

#             return redirect(verify_otp, email=email)

#         except Exception as e:
#             print(str(e))
#             return HttpResponse(str(e))

#     return render(request, 'forgot_password.html')

# def verify_otp(request, email):
#     if request.method == 'POST':
#         otp = request.POST.get('otp')

#         try:
#             temp_reg = TemporaryTable.objects.get(email=email, otp=verify_otp)
#             return redirect(reset_password, email=email)
#         except TemporaryTable.DoesNotExist:
#             messages.error(request, 'Invalid OTP.')
#             return redirect(verify_otp, email=email)

#     return render(request, 'verify_otp.html', {'email': email})

# def reset_password(request, email):
#     if request.method == 'POST':
#         new_password = request.POST.get('new_password')

#         try:
#             user = RegistrationTable.objects.get(email=email)
#             user.password = new_password
#             user.save()

#             try:
#                 server = mail.SMTP("heetlahute@gmail.com", "myuh ajbw mlzu qlvo")
#                 server.send(
#                     to=email,
#                     subject="Password Reset Successful",
#                     contents="Your password has been successfully reset."
#                 )
#                 print("Email Sent Successfully")
#             except Exception as e:
#                 print(str(e))

#             return redirect('success')

#         except RegistrationTable.DoesNotExist:
#             messages.error(request, 'User not found.')
#             return redirect(forgot_password)

#     return render(request, 'reset_password.html', {'email': email})       

# This is where OTPs will be temporarily stored (consider using a more secure solution in production)


# def verify_otp(request, email):
#     if request.method == 'POST':
#         # Collect OTP digits
#         otp = ''.join([request.POST.get(f'o{i}') for i in range(1, 5)])
#         new_password = request.POST.get('new_password')

#         # Validate OTP and reset password if correct
#         if email in otp_storage and otp_storage[email] == otp:
#             user = RegistrationTable.objects.get(email=email)

#             # Assign the new password directly (no hashing)
#             user.password = new_password
#             user.save()

#             # Clear OTP after use
#             del otp_storage[email]

#             # Provide a success message and redirect to login
#             messages.success(
#                 request, "Password reset successfully. Please log in.")
#             # Make sure 'login' is the correct URL name for your login page.
#             return redirect('login')
#         else:
#             messages.error(request, "Invalid OTP or expired.")

#     # Render the OTP verification page with the email passed in the context
#     return render(request, 'verify_otp.html', {'email': email})

# def otp_var(request, email):
#     if request.method == 'POST':

#         otp1 = request.POST.get("o1")
#         otp2 = request.POST.get("o2")
#         otp3 = request.POST.get("o3")
#         otp4 = request.POST.get("o4")

#         final_otp = str(otp1)+""+str(otp2)+""+str(otp3)+""+str(otp4)

#         temp_reg = TemporaryTable.objects.get(email=email, otp=final_otp)

#         try:
#                 if temp_reg:

#                     reg = RegistrationTable(
#                         name=temp_reg.name,
#                         email=temp_reg.email,
#                         phone=temp_reg.phone,
#                         password=temp_reg.password
#                     )
#                     reg.save()

#                     sendmail(request,reg.email)

#                     temp_reg.delete()

#                     return redirect('success')


#         except Exception :
#             messages.error('Invalid')
#             return redirect(otp_var, email=str(email))


#     return render(request , 'templates\otpver.html' , {'email':email})


# def verify(request):
#     if request.method == 'POST':
#         name = request.POST.get("name")
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         phone = request.POST.get("phone")

#         reg = RegistrationTable(name=name, email=email, password=password, phone=phone)
#         reg.save()
#         print("hello")

#     try:

#             rand_num = rand.randint(999, 10000)
#             otp = f"{rand_num}"
#             # with open("otp.html", "r") as file:
#             #     html_content = file.read()

#             #dynamic_html = html_content.replace( "<!-- Replace with dynamic OTP -->",f"<div class='otp'>{otp}</div>")
#             smtp_server = mail.SMTP("heetlahute@gmail.com", "myuh ajbw mlzu qlvo")

#             if request.method == 'POST':
#                 user_email = request.POST.get('email')
#                 with open("data.txt","w") as f:
#                     f.write(str(user_email))

#                 #user = RegistrationTable.objects.get(email = email)
#             smtp_server.send(
#                 to=user_email,
#                 subject="OTP Registration",
#                 contents=otp
#             )

#             print("Email sent successfully.")
#             #request.session['user_email'] = user_email

#             return  redirect(otp_var,email=str(user_email))

#     except Exception as e:
#             print(str(e))

#             return HttpResponse(str(e))

    # return render(request,'verify.html')

# def authtication_otp(request):
#     data = "none"

#     if request.method == "POST":
#         otp = request.POST.get("otp_veri")
#         email = request.POST.get("email_veri")
#         print(otp)
#         print(email)

#         data = str(otp)+" "+str(email)

#     return HttpResponse(data)


# def otp_var(request, email):

#     if request.method == 'POST':  # Extract OTP digits from the form
#         otp1 = request.POST.get("o1")
#         otp2 = request.POST.get("o2")
#         otp3 = request.POST.get("o3")
#         otp4 = request.POST.get("o4")

#         final_otp = str(otp1) + str(otp2) + str(otp3) + str(otp4)

#         temp_reg = TemporaryTable.objects.get(email=email, otp=final_otp)

#         try:

#             temp_reg = TemporaryTable.objects.get(email=email, otp=final_otp)
#             reg = RegistrationTable(
#                 name=temp_reg.name,
#                 email=temp_reg.email,
#                 phone=temp_reg.phone,
#                 password=temp_reg.password
#             )

#             reg.save()
#             sendmail(request, reg.email)
#             temp_reg.delete()
#             return redirect('success')

#         except Exception as e:

#             messages.error(request, f'An error occurred: {str(e)}')
#             return redirect('otp_var', email=email)

    # return render(request, 'profile.html', {'user': user})

    # if request.method == 'POST':
    # #     id = request.POST.get('id' , id)
    # #     pname = request.POST.get('name', pname)
    # #     pphone = request.POST.get('phone', pphone)
    #     email = request.POST.get('email', email)

    #     user = RegistrationTable.objects.get(email=email)

    # data ={

    #     'name' : user.name,
    #     'phone' : user.phone,
    #     'email' : user.email

    # }
    # return render(request, 'profile.html',{'user':data} )

    # if request.method == 'POST':
    #     email = request.POST.get('email')
    #     password = request.POST.get('password')

    #     try:
    #         user = RegistrationTable.objects.get(email=email, password=password)
    #         request.session['id'] = user.id

    #         return redirect('home2', id=user.id or 0)

    #     except RegistrationTable.DoesNotExist:
    #        return HttpResponse("Not valid input")

    # return render(request, 'login.html')

    # def login_view(request,id):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')


#         user = RegistrationTable.objects.get(email=email, password=password)

#         if user:
#             print("yes")
#             return redirect('home2')
#         else:
#             print("no")

#     return render(request, 'login.html',{'user':id})
