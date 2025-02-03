from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import TemporaryTable, RegistrationTable, Product, Cart, EditableContent, Home2edit
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import yagmail as mail
import random as rand
from django.contrib.auth.models import User
import json
import logging
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import base64
import io
import os
from io import BytesIO
from django.contrib.auth import logout


import tempfile


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
            return HttpResponse("<h1>User not found</h1>")

    return render(request, 'login.html')


def success(request, id):

    user = RegistrationTable.objects.get(id=id)
    data = {
        'id': id
    }
    return render(request, 'success.html', {'user': data})


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
    content = EditableContent.objects.first()
    with open('con.txt', 'w') as f:
        f.write(str(content))
    return render(request, 'home.html', {'content': content})


def home_2(request, id):
    content = get_object_or_404(Home2edit, pk=1)
    with open('new.txt', 'w') as f:
        f.write(str(content))
    data = {
        'id': id,
        'content': content
    }
    return render(request, "home2.html", data)


def contact(request, id):
    data = {
        'id': id
    }
    return render(request, 'contact.html', {'data': data})


@csrf_exempt
def add_to_cart(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
            product_id = data.get("product_id")
            quantity = int(data.get("quantity", 1))

            print(f"User ID: {user_id}, Product ID: {
                  product_id}, Quantity: {quantity}")

            user = get_object_or_404(RegistrationTable, id=user_id)
            product = get_object_or_404(Product, id=product_id)
            cart_item, created = Cart.objects.get_or_create(
                user=user, product=product)

            if not created:
                cart_item.quantity += int(quantity)
                cart_item.save()
            else:
                cart_item.quantity = int(quantity)
                cart_item.save()

            return JsonResponse({"success": True, "message": "Item added to cart."})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Invalid request."})


def products(request):

    user_id = request.GET.get('user_id')
    print(f"User ID: {user_id}")  # Debugging print statement
    products = Product.objects.all()
    return render(request, "products.html", {"products": products, "user_id": user_id})


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

            temp_reg.delete()

            # Redirect to home2 with the user's ID
            return redirect('home2', id=reg.id)
        except TemporaryTable.DoesNotExist:
            messages.error(
                request, "Invalid OTP or expired OTP. Please try again.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

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


otp_storage = {}


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = RegistrationTable.objects.get(email=email)
            otp = rand.randint(1000, 9999)
            otp_storage[email] = otp

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
            del otp_storage[email]
            messages.success(
                request, "Password reset successfully. Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP or expired.")
    return render(request, 'verify_otp.html', {'email': email})


def cart_page(request, user_id):
    user = get_object_or_404(RegistrationTable, id=user_id)
    cart_items = Cart.objects.filter(user=user)

    total_amount = 0
    for item in cart_items:
        item.total = item.product.price * item.quantity
        total_amount += item.total

    data = {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'user_id': user_id
    }
    return render(request, "cart.html", {"data": data})


@csrf_exempt
def remove_cart_item(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            item = get_object_or_404(Cart, id=item_id)
            item.delete()
            return JsonResponse({"success": True, "message": "Item removed from cart."})
        except Exception as e:
            logger.error(f"Error removing cart item: {str(e)}")
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Invalid request."})


@csrf_exempt
def update_cart_quantity(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            quantity = data.get('quantity')
            item = get_object_or_404(Cart, id=item_id)
            item.quantity = quantity
            item.save()
            return JsonResponse({"success": True, "message": "Quantity updated."})
        except Exception as e:
            logger.error(f"Error updating cart quantity: {str(e)}")
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Invalid request."})


@csrf_exempt
def buy_item(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            item = get_object_or_404(Cart, id=item_id)
            item.purchased = True
            item.save()

            item_data = {
                'id': item.id,
                'product': {
                    'name': item.product.name,
                    'price': item.product.price,
                },
                'quantity': item.quantity,
                'total': item.product.price * item.quantity
            }

            # Delete the item from the cart
            item.delete()

            return JsonResponse({"success": True, "message": "Item purchased successfully.", "item": item_data})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Invalid request."})


@csrf_exempt
def buy_all_items(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            user = get_object_or_404(RegistrationTable, id=user_id)
            cart_items = Cart.objects.filter(user=user)

            items_data = []
            total_amount = 0

            for item in cart_items:
                item.purchased = True
                item.save()
                item_total = item.product.price * item.quantity
                total_amount += item_total
                items_data.append({
                    'id': item.id,
                    'product': {
                        'name': item.product.name,
                        'price': item.product.price,
                    },
                    'quantity': item.quantity,
                    'total': item_total
                })

            # Delete all items from the cart
            cart_items.delete()

            return JsonResponse({
                "success": True,
                "message": "All items purchased successfully.",
                "items": items_data,
                "total_amount": total_amount
            })
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Invalid request."})


def order_summary(request, user_id):
    user = get_object_or_404(RegistrationTable, id=user_id)
    cart_items = Cart.objects.filter(user=user, purchased=True)

    total_amount = 0
    for item in cart_items:
        item.total = item.product.price * item.quantity
        total_amount += item.total

    data = {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'user_id': user_id
    }
    return render(request, "order_summary.html", {"data": data})


@csrf_exempt
def send_email_with_pdf(request):
    if request.method == 'POST':
        try:
            # Retrieve the user ID from the request data
            data = json.loads(request.body)
            user_id = data.get('user_id')

            # Retrieve the user's email from the RegistrationTable
            try:
                user = RegistrationTable.objects.get(id=user_id)
                email = user.email
                with open('email.txt', 'w') as f:
                    f.write(str(email))

            except RegistrationTable.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'User registration not found.'})

            # pdf_data = data.get('pdf_base64')
            # pdf_name = data.get('pdf_name', 'order_summary.pdf')
            pdf_data = data.get('pdf_base64')
            pdf_content = base64.b64decode(pdf_data.split(',')[1])

            with tempfile.NamedTemporaryFile(delete=False, mode='wb') as f:
                f.write(pdf_content)
                temp_pdf_path = f.name

            os.rename(temp_pdf_path, f"{temp_pdf_path}.pdf")

            yag = mail.SMTP('heetlahute@gmail.com', 'myuh ajbw mlzu qlvo')
            yag.send(
                to=email,
                subject='Your Delicious 😋 Order Summary',
                contents='Thank you for your purchase! Please find the attached order summary !! Enjoy the delicious Ice-Cream🍨',
                attachments=[f"{temp_pdf_path}.pdf"]

            )
            os.remove(temp_pdf_path)

            return JsonResponse({'success': True, 'message': 'Email sent successfully.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@csrf_exempt
def home_edit(request):
    content, created = EditableContent.objects.get_or_create(pk=1)
    if request.method == 'POST':
        data = json.loads(request.body)
        content.title = data.get('title', content.title)
        content.subtitle = data.get('subtitle', content.subtitle)
        content.description = data.get('description', content.description)
        content.save()
        return JsonResponse({"success": True, "message": "Content updated successfully."})
    return render(request, 'home_edit.html', {'content': content})


@csrf_exempt
def home2edit(request):
    content, created = Home2edit.objects.get_or_create(pk=1)
    if request.method == 'POST':
        data = json.loads(request.body)
        content.title = data.get('title', content.title)
        content.subtitle = data.get('subtitle', content.subtitle)
        content.description = data.get('description', content.description)
        content.save()
        return JsonResponse({"success": True, "message": "Content updated successfully."})
    return render(request, 'home2edit.html', {'content': content})


def DashBoard(request):
    return render(request, "DashBoard.html")


# def home_edit(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         subtitle = request.POST.get('subtitle')
#         description = request.POST.get('description')
#         editable_content, created = EditableContent.objects.get_or_create()
#         editable_content.title = title
#         editable_content.subtitle = subtitle
#         editable_content.description = description
#         editable_content.save()
#         return redirect('home')
#     editable_content = EditableContent.objects.first()
#     return render(request, 'home_edit.html', {'editable_content': editable_content})
# @csrf_exempt
# def send_email_with_pdf(id):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             # Retrieve the user's email from the RegistrationTable
#             try:
#                 user = RegistrationTable.objects.get(email=email)
#                 with open('email1.txt','w') as f:
#                     f.write(str(email))
#             except RegistrationTable.DoesNotExist:
#                 return JsonResponse({'success': False, 'message': 'User registration not found.'}
#             pdf_data = data.get('pdf_base64')
#             pdf_name = data.get('pdf_name', 'order_summary.pdf')
#             pdf_content = base64.b64decode(pdf_data.split(',')[1])
#             # Send the email logic (example with yagmail)
#             yag = mail.SMTP('heetlahute@gmail.com', 'myuh ajbw mlzu qlvo')
#             yag.send(
#                 to=email,
#                 subject='Your Order Summary',
#                 contents='Thank you for your purchase! Please find the attached order summary.',
#                 attachments={pdf_name: pdf_content}
#             )
#             return JsonResponse({'success': True, 'message': 'Email sent successfully.'})
#         except Exception as e:
#             return JsonResponse({'success': False, 'message': str(e)})
#     return JsonResponse({'success': False, 'message': 'Invalid request method.'})
# @csrf_exempt
# @login_required
# def send_email_with_pdf(request):
#     if request.method == 'POST':
#         try:
#             # Check if the user is authenticated
#             if not request.user.is_authenticated:
#                 return JsonResponse({'success': False, 'message': 'User is not authenticated.'})
#             # Proceed with your logic for authenticated users
#             data = json.loads(request.body)
#             # Retrieve the user's email from the RegistrationTable
#             try:
#                 user_registration = RegistrationTable.objects.get(user=request.user)
#                 user_email = user_registration.email
#             except RegistrationTable.DoesNotExist:
#                 return JsonResponse({'success': False, 'message': 'User registration not found.'})
#             pdf_data = data.get('pdf_base64')
#             pdf_name = data.get('pdf_name', 'order_summary.pdf')
#             pdf_content = base64.b64decode(pdf_data.split(',')[1])Send the email logic (example with yagmail)
#             yag = mail.SMTP('heetlahute@gmail.com', 'myuh ajbw mlzu qlvo')
#             yag.send(
#                 to=user_email,
#                 subject='Your Order Summary',
#                 contents='Thank you for your purchase! Please find the attached order summary.',
#                 attachments={pdf_name: pdf_content}
#             )
#             return JsonResponse({'success': True, 'message': 'Email sent successfully.'})
#         except Exception as e:
#             return JsonResponse({'success': False, 'message': str(e)})
#     return JsonResponse({'success': False, 'message': 'Invalid request method.'}
# def RemoveFromCartView(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             item_id = data.get('item_id')
#             if item_id is None:
#                 return JsonResponse({'success': False, 'message': 'Item ID is required.'}, status=400)
#             cart_item = Cart.objects.get(id=item_id)
#             cart_item.delete()
#             return JsonResponse({'success': True, 'message': 'Item removed from cart.'})
#         except Cart.DoesNotExist:
#             return JsonResponse({'success': False, 'message': 'Item not found in cart.'}, status=404)
#         except json.JSONDecodeError:
#             return JsonResponse({'success': False, 'message': 'Invalid JSON.'}, status=400)
#         except Exception as e:
#             return JsonResponse({'success': False, 'message': str(e)}, status=500)
#     return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)
# def ReduceQuantityView(request):
#     if request.method == 'POST':  # Ensure this view only processes POST requests
#         try:
#             data = json.loads(request.body)
#             item_id = data.get('item_id')
#             if item_id is None:
#                 return JsonResponse({'success': False, 'message': 'Item ID is required.'}, status=400)
#             cart_item = Cart.objects.get(id=item_id)
#             if cart_item.quantity > 1:
#                 cart_item.quantity -= 1
#                 cart_item.save()
#                 new_total = cart_item.quantity * cart_item.product.price
#                 # Recalculate the final total for all items in the cart
#                 final_total_amount = sum(
#                     item.quantity * item.product.price for item in Cart.objects.all()
#                 )
#                 return JsonResponse({
#                     'success': True,
#                     'message': 'Quantity reduced by one.',
#                     'new_quantity': cart_item.quantity,
#                     'new_total': new_total,
#                     'final_total_amount': final_total_amount  # Updated value
#                 })
#             else:
#                 return JsonResponse({'success': False, 'message': 'Quantity cannot be reduced below one.'}, status=400)
#         except Cart.DoesNotExist:
#             return JsonResponse({'success': False, 'message': 'Item not found in cart.'}, status=404)
#         except json.JSONDecodeError:
#             return JsonResponse({'success': False, 'message': 'Invalid JSON.'}, status=400)
#         except Exception as e:
#             return JsonResponse({'success': False, 'message': str(e)}, status=500)
#     return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)
# @csrf_exempt
# def buy_item(request):
#      if request.method == 'POST':
#          try:
#              data = json.loads(request.body)
#              item_id = data.get('item_id')
#              item = get_object_or_404(Cart, id=item_id)
#              item.delete()
#              return JsonResponse({"success": True, "message": "Item purchased successfully."})
#          except Exception as e:
#              return JsonResponse({"success": False, "message": str(e)})
#      return JsonResponse({"success": False, "message": "Invalid request."})
# @csrf_exempt
# def buy_all_items(request):
#      if request.method == 'POST':
#          try:
#              data = json.loads(request.body)
#              user_id = data.get('user_id')
#              user = get_object_or_404(RegistrationTable, id=user_id)
#              cart_items = Cart.objects.filter(user=user)
#              cart_items.delete()
#              return JsonResponse({"success": True, "message": "All items purchased successfully."})
#          except Exception as e:
#              return JsonResponse({"success": False, "message": str(e)})
#      return JsonResponse({"success": False, "message": "Invalid request."})
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
#             messages.error(request, "Invalid OTP or expired."
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
