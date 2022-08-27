from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login , logout
from .models import User
from bidding.views import home

# Create your views here.
def registerUser(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.create_user(
            email = email,
            username = uname,
            password=password,
        )

        user.save()
        login(request,user)
        return redirect('home')
    
    return render(request, "auction/register_user.html")


def loginView(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        username = email
        # return HttpResponse("trying")
        print(username, password)
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse("Wrong email or password")
    
    return render(request, "auction/login.html")

