# Create your views here.
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required 
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction, Stavca, Coment


CATEGORIEN = ["Guns", "Men", "Giorl", "Car", "America", "Fag", "Fli", "Lite"]

def index(request):
    auctions = Auction.objects.all()
    couples_auction_price = []
    for auction in auctions:
        couple = []
        couple.append(auction)
        stavcas = Stavca.objects.filter(auction = auction)
        if stavcas: 
            last_stavca = stavcas.last()
            last_price = int(last_stavca.stavca)           
        else:
            last_price = int(auction.startprice)
        couple.append(last_price)
        couples_auction_price.append(couple)
    return render(request, "auctions/index.html", { 
        #"auctions": auctions,
        "couples_auction_price": couples_auction_price
    })
     
def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            auctions = user.auctions.all()
            return HttpResponseRedirect(reverse("list", args=(user.username, )))
        
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

@login_required
def logout_view(request):    
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required 
def new(request):
    if not request.user.is_authenticated:
        return render(request, "auctions/login.html")
 
    if request.method == "POST":
        if not request.POST["name"]:
            return render(request, "auctions/new.html", {
                "categorien": CATEGORIEN,
                "message": "You have not inputed the auction name!"
            })

        elif not request.POST["startprice"]:
            return render(request, "auctions/new.html", {
                "categorien": CATEGORIEN,
                "message": "You have not inputed the auction startprice!"
            })

        elif not request.POST["categorien"]:
            return render(request, "auctions/new.html", {
                "categorien": CATEGORIEN,
                "message": "You have not inputed the auction categorien!"
            })

        user_id = request.user.id
        user_creator = User.objects.get(pk = user_id)
        auction = Auction(user_creator = user_creator, name = request.POST["name"], 
                          information = request.POST["information"], startprice = request.POST["startprice"], 
                          photo = request.POST["photo"], category = request.POST["categorien"], not_closed = True)
        auction.save()
        return HttpResponseRedirect(reverse("index"))#, args=(auction.id)))

    return render(request, "auctions/new.html", {
        "categorien": CATEGORIEN
    })
    
def auction(request, auction_id):
    if not request.user.is_authenticated:
        return render(request, "auctions/login.html")   

    auction = Auction.objects.get(pk = auction_id)             
    stavcas = Stavca.objects.filter(auction = auction)             
    coments = Coment.objects.filter(auction = auction)       
    user = request.user                                        
    auctions = user.auctions.all()                             
    user_creator = str(auction.user_creator)
    current_user = str(user)
    last_stavca = stavcas.last()                                   
    
    if request.method == "POST":       
        if auction in auctions:                                                   
            user.auctions.remove(auction)            
            user.save()            
        else:
            user.auctions.add(auction) 
            user.save() 
        return HttpResponseRedirect(reverse("list", args = (user.username,)))

    if auction.not_closed == True:   
        if last_stavca:
            actual_price = last_stavca.stavca
        else:
            actual_price = auction.startprice

        return render(request, "auctions/auction.html", {
            "auctions": auctions,
            "auction": auction, 
            "stavcas": stavcas,
            "coments": coments,
            "actual_price": actual_price,
            "user_creator": user_creator,
            "current_user": current_user
        })

    else:
        if last_stavca:
            user_winner = last_stavca.stavca_user            
        else: 
            user_winner = auction.user_creator

        if user == user_winner:
            return render(request, "auctions/auction.html", {
                "auctions": auctions,
                "auction": auction,
                "stavcas": stavcas,
                "coments": coments,
                "message": "Congratulations!"
            })

        if user == auction.user_creator and not last_stavca:
            return render(request, "auctions/auction.html", {
                "auctions": auctions,
                "auction": auction,
                "stavcas": stavcas,
                "coments": coments,
                "message": "No interested buyers were found for your product!"
            })

        return render(request, "auctions/auction.html", {
            "auctions": auctions,   
            "auction": auction,
            "stavcas": stavcas,
            "coments": coments,
        })
        
@login_required
def list(request, user_username):
    if not request.user.is_authenticated:
        return render(request, "auctions/login.html")

    user = User.objects.get(username = user_username)
    auctions = user.auctions.all()
    couples_auction_price = []
    for auction in auctions:
        couple = []
        couple.append(auction)
        stavcas = Stavca.objects.filter(auction = auction)
        if stavcas: 
            last_stavca = stavcas.last()
            last_price = int(last_stavca.stavca)           
        else:
            last_price = int(auction.startprice)
        couple.append(last_price)
        couples_auction_price.append(couple)    
    return render(request, "auctions/list.html", {
        "user.username": user_username,  
        "auctions": auctions,
        "couples_auction_price": couples_auction_price
    }) 

@login_required
def coment(request, auction_id):
    if not request.user.is_authenticated:
        return render(request, "auctions/login.html")

    if request.method == "POST":        
        coment_text = request.POST["coment"]                          
        comenting_user = request.user                                  
        comented_auction = Auction.objects.get(pk = auction_id)        
        new_coment = Coment(coment = coment_text, comenting_user = comenting_user, auction = comented_auction)
        new_coment.save()
        return HttpResponseRedirect(reverse("auction", args = (comented_auction.id,)))

@login_required
def stavca(request, auction_id):
    if not request.user.is_authenticated:
        return render(request, "auctions/login.html")

    if request.method == "POST":
        stavca_value = int(request.POST["stavca"])                         
        stavca_user = request.user                                     
        stavca_auction = Auction.objects.get(pk = auction_id)           
        auction_stavca = Stavca.objects.filter(auction = stavca_auction)   

        if stavca_value <= int(stavca_auction.startprice):
            return render(request, "auctions/auction.html", {                                                        
                "message": "Your stavca is too small",
                "auctions": stavca_user.auctions.all(),
                "auction": stavca_auction, 
                "stavcas": auction_stavca,
                "coments": Coment.objects.filter(auction = stavca_auction)
            })

        for auction_stavcas in auction_stavca:
            if stavca_value <= int(auction_stavca.stavca):
                return render(request, "auctions/auction.html", {                                                        
                    "message": "Your stavca is too small",
                    "auctions": stavca_user.auctions.all(),
                    "auction": stavca_auction, 
                    "stavcas": auction_stavca,
                    "coments": Coment.objects.filter(auction = stavca_auction)
                })

        new_stavca = Stavca(stavca = stavca_value, stavca_user = stavca_user, auction = stavca_auction)   
        new_stavca.save()                                                                          
        return HttpResponseRedirect(reverse("auction", args = (stavca_auction.id,))) 

def categorien(request):
    return render(request, "auctions/categorien.html", {
        "categorien": CATEGORIEN
    })

def category(request, category):
    category = request.GET["categorien"]
    auctions = Auction.objects.filter(category = category)
    couples_auction_price = []
    for auction in auctions:
        couple = []
        couple.append(auction)
        stavcas = Rate.objects.filter(auction = auction)
        if stavcas: 
            last_stavca = stavcas.last()
            last_price = int(last_stavca.stavca)           
        else:
            last_price = int(auction.startprice)
        couple.append(last_price)
        couples_auction_price.append(couple)

    return render(request, "auctions/category.html", {
        "category": category,
        "auctions": auctions,
        "couples_auction_price": couples_auction_price
    })

@login_required
def close(request, auction_id):
    if not request.user.is_authenticated:
        return render(request, "auctions/login.html")

    auction = Auction.objects.get(pk = auction_id)
    user_creator = str(auction.user_creator)
    curent_user = str(request.user)
    if curent_user == user_creator:
        if request.method == "POST":
            auction.not_closed = False
            auction.save()
            return HttpResponseRedirect(reverse("auction", args = (auction.id,)))
