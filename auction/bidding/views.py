import re
from django.shortcuts import render
from .models import product
# Create your views here.
def home(request):
    userLogged = False
    username = ""
    if request.user.is_authenticated:
        username = request.user.username
        userLogged = True
    data = {"userLogged": userLogged, "username": username}


    return render(request, 'auction/home.html', data)

def store(request):

    products = product.objects.all()
    data = {"products":products }
    return render(request, 'auction/store.html', data)
    