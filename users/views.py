from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect based on role
            if user.role == 'CEO':
                return redirect('ceo_dashboard')
            else:
                return redirect('officer_dashboard')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'users/login.html')


def user_logout(request):
    logout(request)
    return redirect('home')
