from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.template import loader
from django.middleware.csrf import get_token
from .models import User
from django.contrib.auth.hashers import make_password, check_password
import time
from .models import Verify_Email,Cart,Uploads
import os
import random
import string
from django.http import StreamingHttpResponse
from django.views.generic import View
import time
from . import helper
import threading

def get_user_cart_filenames(user_name):
    try:
        user_cart = Cart.objects.get(user__name=user_name)
        cart_items = user_cart.cartitem_set.all()
        filenames = [item.filename for item in cart_items]
        return filenames
    except Cart.DoesNotExist:
        return []

def get_cart(request):
    all_carts = Cart.objects.all()
    
    cart_data = []
    for cart in all_carts:
        cart_items = cart.cartitem_set.all()
        cart_data.extend([{'username': cart.user.name, 'filename': item.filename} for item in cart_items])
    
    return JsonResponse({'cart': cart_data})

def verify(request, hash_value):
    try:
        verify_email = Verify_Email.objects.get(hash=hash_value)
        user = User.objects.get(email=verify_email.email)
        request.session.clear()
        request.session["user"]=user
        user.email_verified = 1
        user.save()
        verify_email.delete()
        cart = Cart.objects.create(user=user)

        template = loader.get_template('verified.html')
        return HttpResponse(template.render())  
    except Verify_Email.DoesNotExist:
        return JsonResponse({"message": "Invalid verification link"}, status=400)

def resend(request):
    verification_started = request.session.get("verification_started")
    
    if verification_started and request.session.has_key("user"):
        timer_duration = 10
        
        current_time = time.time()
        last_request_time = request.session.get("last_request_time", current_time)
        elapsed_time = current_time - last_request_time
        
        if elapsed_time >= timer_duration:
            request.session["last_request_time"] = current_time
            
            email = request.session.get("email")
            verify_email, created = Verify_Email.objects.get_or_create(email=email)
            
            if created or not verify_email.hash:
                verify_email.generate_unique_hash()
                send_verification_email(email, verify_email.hash)  
            else:
                verify_email.generate_unique_hash()
                send_verification_email(email, verify_email.hash)  
                
            return redirect("unverified")
        else:
            return HttpResponse("Time has not elapsed yet")
    else:
        return HttpResponse("You're not logged in.")
            

def unverified(request):
    verification_started = request.session.get("verification_started")
    if verification_started and request.session.has_key("user"):
        timer_duration = 10
        current_time = time.time()
        if not request.session.has_key("last_request_time"):
            email = request.session.get("email")
            verify_email, created = Verify_Email.objects.get_or_create(email=email)
            
            if created or not verify_email.hash:
                verify_email.generate_unique_hash()
            send_verification_email(email, verify_email.hash)
        last_request_time = request.session.get("last_request_time", current_time)
        elapsed_time = current_time - last_request_time

        remaining_time = max(timer_duration - elapsed_time, 0)

        request.session["last_request_time"] = current_time

        template = loader.get_template("unverified.html")
        mail=request.session.get("email")
        mail=mail.split("@")
        l=len(mail[0])-1
        formated_email=mail[0][0]+str(l*"*")+"@"+mail[1]
        context = {"email": formated_email, "timer_duration": remaining_time}
        render = template.render(context, request)
        return HttpResponse(render)
    else:
        return HttpResponse("Verification not started or user not logged in")

def send_verification_email(email, hash_value):
    url="http://127.0.0.1:8000/verify/"+str(hash_value)
    helper.send_verification_email(email,url)
    

def logout(request):
    if "user" in request.session:
        request.session.clear()
        return redirect("login")
    else:
        return redirect("login")

def dash(request):
    if request.session.get("user"):
        csrf_token = get_token(request)
        context = {'user': request.session["user"],'csrf_token': csrf_token}
        template = loader.get_template('dash.html')
        rendered_template = template.render(context, request)
        return HttpResponse(rendered_template)
    else:
        return redirect("login")

def index(request):
    request.session["value"]=1
    template = loader.get_template('home.html')
    return HttpResponse(template.render())


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                if user.email_verified:  
                    request.session["user"] = user
                    return JsonResponse({"message": "success"}, status=200)
                if not user.email_verified:
                    request.session["user"] = user
                    request.session["verification_started"]=True
                    request.session["email"]=user.email
                    return JsonResponse({"message": "verify"}, status=200)
                else:
                    return JsonResponse({"message":"Something went wrong:("},status=500)
            else:
                return JsonResponse({"message": "Incorrect password"}, status=401)
        except User.DoesNotExist:
            return JsonResponse({"message": "User does not exist"}, status=404)
        except Exception as e:
            print(str(e))
            return JsonResponse({"message": "Something went wrong:("}, status=500)

    else:
        csrf_token = get_token(request)
        context = {'csrf_token': csrf_token}
        template = loader.get_template('login.html')
        rendered_template = template.render(context, request)
        return HttpResponse(rendered_template)


def signup(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get("confirm")
        if (password != confirm):
            return JsonResponse({"message": "Passwords Doesn't Match :("}, status=500)

        additional_params = request.POST.get('additional_params')
        try:
            new_user = User(name=name, email=email, password=make_password(
                password), additional_params=additional_params)
            new_user.save()
            return JsonResponse({'message': 'success'}, status=200)
        except Exception as e:
            print(str(e))
            return JsonResponse({"message": "Something Went Wrong :("}, status=500)

    else:
        csrf_token = get_token(request)
        context = {'csrf_token': csrf_token}
        template = loader.get_template('signup.html')
        rendered_template = template.render(context, request)
        return HttpResponse(rendered_template)


def profile_upload(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        random_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        _, extension = os.path.splitext(image.name)
        new_filename = random_filename + extension
        
        upload_directory = "main/static/"
        
        os.makedirs(upload_directory, exist_ok=True)
        
        with open(os.path.join(upload_directory, new_filename), 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        
        user = request.session.get("user")
        user.profile = new_filename

        user.save()
        return JsonResponse({'success': True, 'message': 'Image uploaded successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'No image file provided'})

import subprocess

from PIL import Image as PILImage


def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        random_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        _, extension = os.path.splitext(image.name)
        new_filename = random_filename + extension
        
        upload_directory = "main/static/"
        
        os.makedirs(upload_directory, exist_ok=True)
        
        # Resize the image to reduce memory usage
        img = PILImage.open(image)
        img.thumbnail((800, 800))  # Resize the image to a maximum width and height of 800 pixels
        img.save(os.path.join(upload_directory, new_filename))
        
        user = request.session.get("user")
        cart, created = Cart.objects.get_or_create(user=user)
        cart.add_item(filename=new_filename)
        cart.save()
        
        # Launch a detached subprocess to handle image processing
        subprocess.Popen(["python", str(os.getcwd())+"\\main\\process_image.py", str(user.uid), str(user.name),str(user.profile),new_filename])
        
        return JsonResponse({'success': True, 'message': 'Image uploaded successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'No image file provided'})


    
    
def uploads_json(request):
    uploads = Uploads.objects.all()

    data = []
    for upload in uploads:
        data.append({
            'name': upload.name,
            'filename': upload.filename,
            "profile":upload.profile_name,
            'tags': upload.tags,
        })

    return JsonResponse(data, safe=False)

def notify(request):
    try:
        val=1
        return JsonResponse({"value":str(val)})
    except:
        return JsonResponse({"value":str(0)})
    