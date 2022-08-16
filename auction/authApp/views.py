from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login , logout
from .models import *
from bidding.views import home
# Create your views here.
def registerUser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.create_user(
            username = username,
            email = email,
            password = password
        )

        user.save()
        login(request,user)
    
    return home(request)