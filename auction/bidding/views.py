import re
from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponse
from .models import product as productModel
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

    data = {"product":prod}
    return render(request, "auction/product.html", data)



def bid(request, id):
    if request.method == "POST":
        data = {}
        prod = product.objects.get(pid=id)
        curPrice = prod.price
        bidPrice = request.POST.get("bidPrice")
        if bidPrice < curPrice*(101/100) :
            return HttpResponse("minimum price bid critera is not begin fullfiled")
        
        latestBid = bid(
            bidder = request.user,
            product = prod,
            prevPrice = curPrice,
            curPrice = bidPrice

        )
        latestBid.save()
        return render(request, 'auction/product.html', data)
    