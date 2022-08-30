import re
from unicodedata import decimal
from django.shortcuts import render, redirect
from django.http.response import JsonResponse, HttpResponse
from .models import product as productModel, bid as bidModel
from authApp.models import userProfile
from datetime import datetime
# Create your views here.

def check_completion():
    completedProd = productModel.objects.filter(deadline__lte = datetime.now(), complete=False)
    print(completedProd)
    for prod in completedProd:
        seller = prod.seller
        seller = userProfile.objects.get(user= seller)
        bids = bidModel.objects.filter(product=prod, active=True)
        if len(bids) > 0:
            lastBid = bids[0]
            seller.balance += lastBid.curPrice
            lastBid.successfull = True
            lastBid.save()
        prod.complete = True
        seller.save()
        prod.save()



def home(request):
    check_completion()
    userLogged = False
    username = ""
    if request.user.is_authenticated:
        username = request.user.username
        userLogged = True
    data = {"userLogged": userLogged, "username": username}


    return render(request, 'auction/home.html', data)

def store(request):
    check_completion()
    if request.method == "POST":
        queryString = request.POST.get("query")
        res = productModel.objects.filter(name__icontains=queryString)
        data = {"products":res }
        return render(request, 'auction/store.html', data)

    products = productModel.objects.all()
    data = {"products":products }
    return render(request, 'auction/store.html', data)

def product(request, id):
    check_completion()
    prod = productModel.objects.get(pid=id)
    curPrice = prod.curPrice
    minBid = (curPrice*101)//100 +1
    data = {"product":prod, "minBid" : minBid}
    return render(request, "auction/product.html", data)



def bid(request, id):
    check_completion()
    print("in bid")
    if not request.user.is_authenticated:
        return render(request,"auction/login.html")
    if request.method == "POST":
        print("in bid post")
        data = {}
        prod = productModel.objects.get(pid=id)
        curPrice = prod.curPrice
        bidPrice = float(request.POST.get("bidPrice"))
        if prod.complete:
            return HttpResponse("Auction finished for this product")
        if bidPrice < (curPrice*101)//100 +1 :
            return HttpResponse("minimum price bid critera is not begin fullfiled")
        curUser = userProfile.objects.get(user = request.user)
        if curUser.balance < bidPrice:
            return HttpResponse("not enough balance")
        curUser.balance -= bidPrice
        print(curUser)
        lastBid = bidModel.objects.all().filter(product=prod, active=True)
        if len(lastBid) > 0:
            lastBid = lastBid[0]
            print("last bid exists")
            lastBid.active = False
            lastBidder = userProfile.objects.get(user = lastBid.bidder)

            print("adding " ,lastBidder.balance ,lastBid.curPrice)
            lastBidder.balance += lastBid.curPrice
            print(lastBidder.balance, "is the new balance")
            lastBidder.save()
            lastBid.save()
        else:
            print("no last bid")


        data["minBid"] = curPrice*(101//100) +1
        prod.prevPrice = curPrice
        prod.curPrice = bidPrice
        prod.save()

        latestBid = bidModel(
            bidder = request.user,
            product = prod,
            prevPrice = curPrice,
            curPrice = bidPrice

        )
        latestBid.save()
        curUser.save()
        return product(request, prod.pid)

def userInfo(request):
    check_completion()
    if not request.user.is_authenticated:
        return render(request, "auction/login.html")
    
    userp = userProfile.objects.get(user=request.user)
    data = {"user" : userp}
    return render(request, "auction/userInfo.html",data)

def addBalance(request):
    check_completion()
    if not request.user.is_authenticated:
        return render(request, "login.html")
    curUser = userProfile.objects.get(user=request.user)
    amount = request.POST.get("balance")
    print(amount)
    print(request.POST)
    curUser.balance += float(amount)
    curUser.save()
    return userInfo(request)

def allBidView(request):
    check_completion()
    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    allBids = bidModel.objects.filter(bidder=request.user)
    data = {"allBid" : allBids}

    return render(request,"auction/bidHistory.html", data)

def myProducts(request):
    check_completion()
    if not request.user.is_authenticated:
        return render(request, "login.html")

    products =  productModel.objects.filter(seller=request.user)
    data = {"products":products}
    return render(request,"auction/myProducts.html", data)

def addProduct(request):
    if not request.user.is_authenticated:
        return render(request, "auction/login.html")
    if request.method == "POST":
        pname = request.POST.get("pname")
        price = request.POST.get("price")
        age = request.POST.get("age")
        description = request.POST.get("description")
        deadline = request.POST.get("deadline")
        image = request.FILES.get("image")
        print(deadline)
        return HttpResponse("success")
        newProduct = productModel(
            name = pname,
            basePrice = price,
            curPrice = price,
            age = age,
            description = description,
            deadline = deadline,
            seller = request.user
        )
        return redirect("userInfo")
    return render(request, "auction/addProduct.html")
