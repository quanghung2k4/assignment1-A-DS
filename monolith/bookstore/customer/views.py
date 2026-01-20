from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Customer


def register_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        if not (name and email and password and confirm):
            messages.error(request, "Please fill all fields.")
        elif password != confirm:
            messages.error(request, "Passwords do not match.")
        elif Customer.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
        else:
            hashed = make_password(password)
            customer = Customer.objects.create(name=name, email=email, password=hashed)
            request.session["customer_id"] = customer.id
            messages.success(request, "Registration successful.")
            return redirect("home")

    return render(request, "accounts/register.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            customer = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            customer = None

        if customer and check_password(password, customer.password):
            request.session["customer_id"] = customer.id
            messages.success(request, "Logged in successfully.")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, "accounts/login.html")


def logout_view(request):
    request.session.pop("customer_id", None)
    messages.info(request, "Logged out.")
    return redirect("home")
from django.shortcuts import render

# Create your views here.
