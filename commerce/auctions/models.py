from django.contrib.auth.models import AbstractUser
from django.db import models


class Listing(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=64)
    image = models.ImageField(upload_to='listings', blank=True)
    description = models.CharField(max_length=512)
    

class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=64)
    email = models.EmailField()
    listings = models.ManyToManyField(Listing, blank=True, related_name='user_listings')
    balance = models.IntegerField()

class Bid(models.Model):
    id = models.BigAutoField(primary_key=True)
    current_bid = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_bids')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listing_bid')

class Comments(models.Model):
    id = models.BigAutoField(primary_key=True)
    text = models.CharField(max_length=512)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listing_comments')
