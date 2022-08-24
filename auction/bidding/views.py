import re
from django.shortcuts import render

# Create your views here.
def home(request):
    userLogged = False
    username = ""
    if request.user.is_authenticated:
        username = request.user.username
        userLogged = True
    data = {"userLogged": userLogged, "username": username}


    return render(request, 'auction/home.html', data)
    