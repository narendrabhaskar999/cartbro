from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Customer
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

def sign_out(request):
    logout(request)
    return redirect('home')

def show_account(request):
    context={}
    if request.method == 'POST' and 'register' in request.POST:
        context['register']=True
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("account")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect("account")

        try:
            # Creates user account (with hashed password)
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )

            # Creates customer profile linked to the user
            customer = Customer.objects.create(
                user=user,
                phone=phone,
                address=address,
                delete_status=False
            )

            messages.success(request, "User registered successfully!")
            return redirect("account")  # Redirect to home page after success

        except Exception as e:
            messages.error(request, "Error: "+str(e))
            return redirect("account")
        
    if request.method == 'POST' and 'login' in request.POST:
        context['register']=False
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user=authenticate(username=username,password=password)
        
        if user is not None:
            login(request,user)
            messages.success(request, "Login successful!")
            return redirect('home')
        else:
            messages.error(request, " Invalid User Credentials! ")

    return render(request, "account.html",context)
