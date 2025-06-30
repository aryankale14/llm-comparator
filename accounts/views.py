from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import messages




def signup_view(request):
    if request.method == "POST":
        username= request.POST["username"]
        password= request.POST["password"]
        email=request.POST["email"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("signup")

        user= User.objects.create_user(username=username, password=password, email=email)
        login(request, user)
        #messages.success(request, "Signup successful! You are now logged in.")
        return redirect("home")

    return render(request, "accounts/signup.html")


def login_view(request):
    if request.method == "POST":
        username= request.POST["username"]
        password= request.POST["password"]

        user= authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            #messages.success(request, "Login successful!")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials.")
            return redirect("login")
    
    return render(request, "accounts/login.html")


def logout_view(request):
    if request.method == "POST":
        logout(request)
        #messages.success(request, "You have been logged out.")
        return redirect("login")
    return redirect("home")
