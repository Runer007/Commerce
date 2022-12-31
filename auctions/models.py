# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class Auction(models.Model):
    user_creator = models.CharField(max_length = 64)
    name = models.CharField(max_length = 100, blank = False)
    information = models.TextField(blank = False)
    startprice = models.IntegerField(blank = False)
    photo = models.URLField()
    category = models.CharField(max_length = 64, blank = False)
    not_closed = models.BooleanField(default = True)

    

class User(AbstractUser): 
    auctions = models.ManyToManyField(Auction, blank = True, related_name = "users")

    


class Stavca(models.Model):    
    stavca = models.IntegerField()   
    stavca_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "stavca")
    auction = models.ForeignKey(Auction, on_delete = models.CASCADE, related_name = "stavca_auction")




class Coment(models.Model):    
    coment = models.TextField()
    comenting_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "coments")
    auction = models.ForeignKey(Auction, on_delete = models.CASCADE, related_name = "coment_auction")

   