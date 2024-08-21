from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required 
from json import dumps,dump

from .models import *

def Find_max_bid(Bids):
    maxBid = Bids.first()
    for b in Bids:
        if b.bid > maxBid.bid:
            maxBid = b
    return maxBid


def index(request):
    user=request.user
    listings=Listing.objects.all()
    return render(request, "auctions/index.html",{
        "allListings":listings,
        "user":user
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
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

def create_listing(request):
    if request.method == "GET":
        categories=Category.objects.all()
        sub_categories=SubCategory.objects.all()


        return render(request,"auctions/create_new_listing.html",{
            'categories':categories,
            'SubCategories':sub_categories
        })
    else:
        currentUser=request.user
        title=request.POST['Title']
        starting_price=request.POST['Staring_price']
        imageurl=request.POST['imageurl']
        description=request.POST['detailed_description']
        category=request.POST['Category']
        subCategory=request.POST['sub_category']
        milage=request.POST["Milage"]
        color=request.POST['Color']
        location=request.POST['Location']
        condition=request.POST['Condition']
        ModelYear=request.POST['ModelYear']
        Model_Trim=request.POST['Model_Trim']

        categoryData=Category.objects.get(categoryName=category)
        subCategoryData=SubCategory.objects.get(subCategoryName=subCategory)

        New_Listing=Listing(
            owner=currentUser,
            title=title,
            starting_bid_price=starting_price,
            imageURL=imageurl,
            detailed_description=description,
            category=categoryData,
            subCategory=subCategoryData,
            Location=location,
            Color=color,
            Milage=milage,
            condition=condition,
            Model_Trim=Model_Trim,
            ModelYear=ModelYear
            )

        New_Listing.save()

        image1 = Image(listing=New_Listing,image=New_Listing.imageURL)
        image1.save()


        return HttpResponseRedirect(reverse('index'))

def display_watchlist(request,user_id):
    user = User.objects.get(id=user_id)
    watchlist_listings = Watchlist.objects.filter(user=user)

    return render(request, 'auctions/display-watchlist.html', {
        'Page_Heading':f"{user.username.title()}'s Watchlist",
        'watchlist_listings':watchlist_listings,
    })

def display_categories(request):
    if request.method == "GET":
        categories = Category.objects.all()
        subCategories = SubCategory.objects.all()

        return render(request, 'auctions/categories.html',{
            "categories":categories,
            "subCategories":subCategories
        })
    else:
        categoryDataSet=request.POST.getlist('categories[]')
        selectcategories = Category.objects.filter(categoryName__in=categoryDataSet)

        subCategoryDateSet=request.POST.getlist('subCategories[]')
        selectsubCategories=SubCategory.objects.filter(subCategoryName__in=subCategoryDateSet)

        if selectcategories.exists():
            allListings=Listing.objects.filter(category__in=selectcategories)
        elif selectsubCategories.exists():
            allListings=Listing.objects.filter(subCategory__in=selectsubCategories)
        else:
            allListings=Listing.objects.filter(subCategory__in=selectsubCategories,category__in=selectcategories)

        categories=Category.objects.all()
        subCategories=SubCategory.objects.all()
        
        return render(request,'auctions/category-listings.html',{
           "categories":categories,
           "subCategories":subCategories,
           "allListings":allListings
        })

def display_cart(request,user_id):
    user = User.objects.get(id=user_id)
    cart_listings = Cart.objects.filter(cart_user=user)

    return render(request, 'auctions/display-watchlist.html', {
        'Page_Heading':f"{user.username.title()}'s Cart",
        'cart_listings':cart_listings,
    })

def display_listing(request,listing_id,listing_title):
    listing=Listing.objects.get(id=listing_id,title=listing_title)
    user=request.user

    if user != listing.owner:
        listing.views += 1
        
    user_id = listing.owner.id
    listing.save( )
    images=Image.objects.filter(listing=listing)
    comments=Comment.objects.filter(listing=listing)
    Bids = Bid.objects.filter(listing=listing)
    maxBid = Find_max_bid(Bids=Bids)
    data={
        'listing_id':dumps(listing_id),
        'user_id':dumps(user_id)
    }
    dataJSON=dumps(data)
    return render(request,'auctions/Listing.html',{
        'title':f"{listing.ModelYear} {listing.title.title()} {listing.Model_Trim.title()}",
        'listing':listing,
        "comments":comments,
        'user':user,
        'images':images,
        'data':dataJSON,
        'maxBid':maxBid,
        'Bids':Bids

    })

def Place_Bid(request,listing_id,Bidder_id):
    listing=Listing.objects.get(id=listing_id)
    comments=Comment.objects.filter(listing=listing)
    images=Image.objects.filter(listing=listing)

    data = {
    'listing_id':dumps(listing_id),
    'user_id':dumps(Bidder_id)
    }

    dataJSON=dumps(data)

    if request.method == "GET":
        return HttpResponseRedirect(reverse('display_listing',args=[listing_id,listing.title]))

    else:
        offer=float(request.POST['bid'])
        starting_price = listing.starting_bid_price
        bidder=User.objects.get(id=Bidder_id)
        Bids=Bid.objects.filter(listing=listing,bidder=bidder)
        maxBid = Find_max_bid(Bids=Bids)
        message = ''
        error=''


        if offer >= starting_price:
            if Bids.exists():
                if offer > maxBid.bid:
                    New_bid = Bid(listing=listing,bidder=bidder,bid=offer)
                    New_bid.save()
                    message=f'Bid of ${offer} made by {bidder.username}'
                    return render(request,'auctions/Listing.html',{
                        'title':f"{listing.ModelYear} {listing.title.title()} {listing.Model_Trim.title()}",
                        'user':request.user,
                        'listing':listing,
                        "comments":comments,
                        'message':message,
                        'images':images,
                        'data':dataJSON,
                        'maxBid':New_bid,
                        'Bids':Bids
                    })
                else:
                    error = f"Offer of ${offer} is too low! Offer must be greater than current best offer"
                    return render(request,'auctions/Listing.html',{
                        'title':f"{listing.ModelYear} {listing.title.title()} {listing.Model_Trim.title()}",
                        'user':request.user,
                        'listing':listing,
                        "comments":comments,
                        'error':error,
                        'images':images,
                        'data':dataJSON,
                        'maxBid':maxBid,
                        'Bids':Bids
                    })
            else:
                New_bid = Bid(listing=listing,bidder=bidder,bid=offer)
                New_bid.save()
                message=f'Bid of ${offer} made by {bidder.username}'
                return render(request,'auctions/Listing.html',{
                    'title':f"{listing.ModelYear} {listing.title.title()} {listing.Model_Trim.title()}",
                    'user':request.user,
                    'listing':listing,
                    "comments":comments,
                    'message':message,
                    'images':images,
                    'data':dataJSON,
                    'maxBid':New_bid,
                    'Bids':Bids
                })
        else:
            error = f"Offer of ${offer} is too low! Offer must be atleast equal, if not greater than list price"
            return render(request,'auctions/Listing.html',{
                'title':f"{listing.ModelYear} {listing.title.title()} {listing.Model_Trim.title()}",
                'user':request.user,
                'listing':listing,
                "comments":comments,
                'error':error,
                'images':images,
                'data':dataJSON,
                'maxBid':maxBid,
                'Bids':Bids
            })

def Place_Comment(request,listing_id,commenter_id):
    listing=Listing.objects.get(id=listing_id)
    comments=Comment.objects.filter(listing=listing)
    images=Image.objects.filter(listing=listing)
    Bids = Bid.objects.filter(listing=listing)
    maxBid = Find_max_bid(Bids=Bids)

    dataJSON = dumps({'listing_id':dumps(listing_id),
            'user_id':dumps(commenter_id)})

    if request.method == "GET":
        return HttpResponseRedirect(reverse('display_listing',args=[listing_id,listing.title]))
    else:
        commenter=User.objects.get(id=commenter_id)
        comment=request.POST['comment']

        NewComment = Comment(comment=comment,commenter=commenter,listing=listing)
        NewComment.save()

        return render(request,'auctions/Listing.html',{
            'title':f"{listing.ModelYear} {listing.title.title()} {listing.Model_Trim.title()}",
            'user':request.user,
            'listing':listing,
            "comments":comments,
            'images':images,
            'data':dataJSON,
            'maxBid':maxBid,
            'Bids':Bids
        })

def Add_Image(request,listing_id):
    listing=Listing.objects.get(id=listing_id)
    comments=Comment.objects.filter(listing=listing)
    images=Image.objects.filter(listing=listing)
    user_id=listing.owner.id
    Bids = Bid.objects.filter(listing=listing)
    maxBid = Find_max_bid(Bids=Bids)

    dataJSON = dumps({'listing_id':dumps(listing_id),
            'user_id':dumps(user_id)})

    if request.method == "GET":
        return HttpResponseRedirect(reverse('display_listing',args=[listing_id,listing.title]))

    else:
        if not Image.objects.filter(listing=listing).exists():
            newImage = Image(listing=listing,image=listing.imageURL)
            newImage.save()

        image = request.POST['addImage']
        newImage = Image(listing=listing,image=image)
        newImage.save()

        return render(request,'auctions/Listing.html',{
            'title':f"{listing.ModelYear} {listing.title.title()} {listing.Model_Trim.title()}",
            'user':request.user,
            'listing':listing,
            "comments":comments,
            'images':images,
            'data':dataJSON,
            'maxBid':maxBid,
            'Bids':Bids
    })

def Toggle_Watchlist_status(request,listing_id,user_id):
    listing = Listing.objects.get(id=listing_id)
    user=User.objects.get(id=user_id)
    comments=Comment.objects.filter(listing=listing)
    images=Image.objects.filter(listing=listing)
    Bids = Bid.objects.filter(listing=listing)
    maxBid = Find_max_bid(Bids=Bids)

    dataJSON = dumps({'listing_id':dumps(listing_id),
            'user_id':dumps(user_id)})
    
    Watchlist_listing = Watchlist.objects.filter(listing=listing,user=user)

    if request.method == 'GET':
        return HttpResponseRedirect(reverse('display_listing',args=[listing_id,listing.title]))
    else:
        if Watchlist_listing.exists():
            Watchlist_listing.delete()
            listing.watches -= 1
            listing.save()
        else:
            Watchlist_listing = Watchlist(listing=listing,user=user)
            Watchlist_listing.save()
            listing.watches += 1
            listing.save()

        return render(request,'auctions/Listing.html',{
                'title':f"{listing.ModelYear} {listing.title.title()} {listing.Model_Trim.title()}",
                'user':request.user,
                'listing':listing,
                "comments":comments,
                'images':images,
                'data':dataJSON,
                'maxBid':maxBid,
                'Bids':Bids
            })

def Cart_Listing(request,listing_id):
    listing = Listing.objects.get(id=listing_id)
    listing.isActive = False

    currentUser = request.user

    Bids = Bid.objects.filter(listing=listing)
    winningBid = Find_max_bid(Bids=Bids)
    winningBidder = winningBid.bidder
    Cart_listing = Cart(listing=listing,cart_user=winningBidder)
    Cart_listing.save()


    comments = Comment.objects.filter(listing=listing)
    images = Image.objects.filter(listing=listing)

    if currentUser != winningBidder:
        message=f"Bid for {listing.title.title()} won by {winningBidder.username.upper()}, with a bid of: ${winningBid.bid}"
    else:
        message=f"You have won the bid for {listing.title.title()}, with a bid of: ${winningBid.bid}"

    return render(request,'auctions/Listing.html',{
        'title':f"{listing.ModelYear} {listing.title.title()} {listing.Model_Trim.title()}",
        'user':request.user,
        'listing':listing,
        "comments":comments,
        'images':images,
        'maxBid':winningBid,
        'Bids':Bids
    })

