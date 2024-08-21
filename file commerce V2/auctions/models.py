from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName=models.CharField(max_length=64)

    def __str__(self):
        return self.categoryName
    
class SubCategory(models.Model):
    subCategoryName=models.CharField(max_length=64) 

    def __str__(self):
        return self.subCategoryName

class Listing(models.Model):
    title=models.CharField(max_length=100)
    detailed_description=models.TextField(max_length=1000)
    Milage=models.IntegerField()
    ModelYear=models.IntegerField()
    Model_Trim=models.CharField(max_length=200)
    Location=models.CharField(max_length=100)
    Color=models.CharField(max_length=100)
    starting_bid_price=models.FloatField()
    imageURL=models.ImageField()
    isActive=models.BooleanField(default=True)
    owner=models.ForeignKey(User,related_name='owner',on_delete=models.CASCADE,blank=True,null=True)
    category=models.ForeignKey(Category,related_name='Item_Category',blank=True,null=True,on_delete=models.CASCADE)
    subCategory=models.ForeignKey(SubCategory,related_name='Item_Sub_Category',blank=True,null=True,on_delete=models.CASCADE)
    views=models.IntegerField(default=0)
    watches=models.IntegerField(default=0)
    condition=models.CharField(max_length=64)

    def __str__(self) :
        return f"{self.title.upper()} {self.Model_Trim.upper()}"
    
class Bid(models.Model):
    bidder=models.ForeignKey(User,related_name='bidder',on_delete=models.CASCADE,blank=True,null=True)
    bid=models.FloatField()
    listing=models.ForeignKey(Listing,related_name="listing_bid",on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return f'{self.bidder.username.upper()}: Bid = US $ {self.bid}'

class Cart(models.Model):
    cart_user=models.ForeignKey(User,related_name='cart_user',on_delete=models.CASCADE,blank=True,null=True)
    listing=models.ForeignKey(Listing,related_name="carted_listing",on_delete=models.CASCADE,blank=True,null=True)

class Comment(models.Model):
    commenter=models.ForeignKey(User,related_name='commenter',on_delete=models.CASCADE,blank=True,null=True)
    comment=models.TextField(max_length=150)
    listing=models.ForeignKey(Listing,related_name="listing_comment",on_delete=models.CASCADE,blank=True,null=True)


    def __str__(self):
        return f'''{self.commenter.username.upper()}:- {self.comment}'''
    
class Image(models.Model):
    listing=models.ForeignKey(Listing,related_name="listing_image",on_delete=models.CASCADE,blank=True,null=True)
    image=models.ImageField()

    def __str__(self):
        return f'{self.listing.title}/Image/{self.id}'

class Watchlist(models.Model):
    listing=models.ForeignKey(Listing,related_name="watchlist_listing",on_delete=models.CASCADE,blank=True,null=True)
    user=models.ForeignKey(User,related_name='watchlist_user',on_delete=models.CASCADE,blank=True,null=True)
    
    def __str__(self):
        return f'Watchlist Listing: {self.listing.title}: User: {self.user}'