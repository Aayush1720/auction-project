import re
from unicodedata import decimal
from django.shortcuts import render, redirect
from django.http.response import JsonResponse, HttpResponse
from .models import product as productModel, bid as bidModel
from authApp.models import userProfile
from datetime import datetime
# Create your views here.

# view which just checks if any of the auction prodcuts have finsihed their deadlines
# if yes then process the respective transactions
def check_completion():
    
    # get all the products which have compoelted their deadlines
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



# return the home page along with required data
def home(request):
    userLogged=False
    username = ""
    check_completion()
    userLogged = False
    username = ""
    if request.user.is_authenticated:
        username = userProfile.objects.get(user=request.user).First_Name
        userLogged = True
    data = {"authenticated": userLogged, "name": username}


    return render(request, 'auction/home.html', data)

# processes get and post requests on store page which incldues searching
def store(request):
    userLogged=False
    username = ""
    if request.user.is_authenticated:
        username = userProfile.objects.get(user=request.user).First_Name
        userLogged = True
    data = {"authenticated": userLogged, "name": username}
    check_completion()
    res = productModel.objects.filter(complete=False)
    if request.method == "POST":
        queryString = request.POST.get("query")
        res = productModel.objects.filter(name__icontains=queryString, complete=False)
        data["products"] = res 
        return render(request, 'auction/store.html', data)

    products = productModel.objects.all()
    data["products"] = res 
    return render(request, 'auction/store.html', data)


# returns a page with packed product depending on the product id
def product(request, id):
    userLogged=False
    username = ""
    if request.user.is_authenticated:
        username = userProfile.objects.get(user=request.user).First_Name
        userLogged = True
    data = {"authenticated": userLogged, "name": username}
    check_completion()
    prod = productModel.objects.get(pid=id)
    curPrice = prod.curPrice
    minBid = (curPrice*101)//100 +1
    data.update({"product":prod, "minBid" : minBid})
    return render(request, "auction/product.html", data)


# processes a bid based on the price and the id of product bid
def bid(request, id):
    userLogged=False
    username = ""
    if request.user.is_authenticated:
        username = userProfile.objects.get(user=request.user).First_Name
        userLogged = True
    data = {"authenticated": userLogged, "name": username}
    check_completion()
    print("in bid")
    if not request.user.is_authenticated:
        return render(request,"auction/login.html")
    if request.method == "POST":
        print("in bid post")
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

# gets the user information from the database and packs it on the user info page
def userInfo(request):
    userLogged=False
    username = ""
    if request.user.is_authenticated:
        username = userProfile.objects.get(user=request.user).First_Name
        userLogged = True
    data = {"authenticated": userLogged, "name": username}
    check_completion()
    if not request.user.is_authenticated:
        return render(request, "auction/login.html")
    
    userp = userProfile.objects.get(user=request.user)
    data.update({"user" : userp})
    return render(request, "auction/userInfo.html",data)

# adds balance to accounts 
def addBalance(request):
    userLogged=False
    username = ""
    if request.user.is_authenticated:
        username = userProfile.objects.get(user=request.user).First_Name
        userLogged = True
    data = {"authenticated": userLogged, "name": username}
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


# packs of all the biddings done by a user on a table and sends it  
def allBidView(request):
    userLogged=False
    username = ""
    if request.user.is_authenticated:
        username = userProfile.objects.get(user=request.user).First_Name
        userLogged = True
    data = {"authenticated": userLogged, "name": username}
    check_completion()
    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    allBids = bidModel.objects.filter(bidder=request.user)
    data.update({"allBid" : allBids})

    return render(request,"auction/bidHistory.html", data)

# gets all the products listed by one user and sends it in a template
def myProducts(request):
    userLogged=False
    username = ""
    if request.user.is_authenticated:
        username = userProfile.objects.get(user=request.user).First_Name
        userLogged = True
    data = {"authenticated": userLogged, "name": username}
    check_completion()
    if not request.user.is_authenticated:
        return render(request, "login.html")

    products =  productModel.objects.filter(seller=request.user)
    data.update({"products":products})
    return render(request,"auction/myProducts.html", data)

# responds when a user lists a new product with all the details about it
def addProduct(request):
    userLogged=False
    username = ""
    if request.user.is_authenticated:
        username = userProfile.objects.get(user=request.user).First_Name
        userLogged = True
        print(userLogged)
    data = {"authenticated": userLogged, "name": username}
    if not request.user.is_authenticated:
        return render(request, "auction/login.html")
    if request.method == "POST":
        pname = request.POST.get("pname")
        price = request.POST.get("price")
        age = request.POST.get("age")
        description = request.POST.get("description")
        deadline = request.POST.get("deadline")
        image = request.FILES.get("image")
        print(request.FILES)
        print(type(image))
        print(image)
        #2022-08-07T22:58
        deadline = datetime.strptime(deadline, '%Y-%m-%dT%H:%M')
        print(deadline)
        newProduct = productModel(
            name = pname,
            basePrice = price,
            curPrice = price,
            age = age,
            description = description,
            deadline = deadline,
            seller = request.user,
            image1 = image
        )
        newProduct.save()
        return redirect("userInfo")
    return render(request, "auction/addProduct.html",data)
