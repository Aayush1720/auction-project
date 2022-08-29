import re
from unicodedata import decimal
from django.shortcuts import render, redirect
from django.http.response import JsonResponse, HttpResponse
from .models import product as productModel, bid as bidModel
from authApp.models import userProfile
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

    products = productModel.objects.all()
    data = {"products":products }
    return render(request, 'auction/store.html', data)

def product(request, id):
    prod = productModel.objects.get(pid=id)
    curPrice = prod.curPrice
    minBid = (curPrice*101)//100 +1
    data = {"product":prod, "minBid" : minBid}
    return render(request, "auction/product.html", data)



def bid(request, id):
    print("in bid")
    if request.method == "POST":
        print("in bid post")
        data = {}
        prod = productModel.objects.get(pid=id)
        curPrice = prod.curPrice
        bidPrice = float(request.POST.get("bidPrice"))
        if bidPrice < (curPrice*101)//100 +1 :
            return HttpResponse("minimum price bid critera is not begin fullfiled")
        
        latestBid = bidModel(
            bidder = request.user,
            product = prod,
            prevPrice = curPrice,
            curPrice = bidPrice

        )
        data["minBid"] = curPrice*(101//100) +1
        prod.prevPrice = curPrice
        prod.curPrice = bidPrice
        prod.save()
        return product(request, prod.pid)

def userInfo(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    userp = userProfile.objects.get(user=request.user)
    data = {"user" : userp}
    return render(request, "auction/userInfo.html",data)

def addBalance(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    curUser = userProfile.objects.get(user=request.user)
    amount = request.POST.get("balance")
    print(amount)
    print(request.POST)
    curUser.balance += decimal(float(amount))
    curUser.save()
    return userInfo(request)