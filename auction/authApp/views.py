from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login , logout
from .models import userProfile
from django.contrib.auth.models import User
from bidding.views import home

# Create your views here.
def registerUser(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username =email)
            return HttpResponse("Account present with thaat email, please login to that account")
        except User.DoesNotExist:
            user = User.objects.create_user(email,password=password)
            login(request,user)
            newUserProfile = userProfile(
                email = email,
                user = user,
                First_Name = fname,
                Last_Name = lname
            )
            newUserProfile.save()
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
        user = authenticate(username=username,password = password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse("Wrong email or password")
    
    return render(request, "auction/login.html")

def logout(request):
    if(request.user.is_authenticated):
        logout(request)

    return redirect('home')

