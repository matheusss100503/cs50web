from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *


def index(request):
    return render(request, "network/index.html")


@login_required(login_url='login')
def following(request):
    return render(request, 'network/following.html')


def posts(request, group):
    if group == 'all_posts':
        posts = Posts.objects.all()

    elif group == 'following':
        try:
            # Gets all the users that the user follows
            following = Follow.objects.filter(user = request.user)

            # Gets the first user from the following list
            posts = Posts.objects.filter(owner = following[0].follows)  

            # Loops through the following list and joins the posts from followed users
            for follow in following[1:]:
                post = Posts.objects.filter(owner = follow.follows)
                posts = posts.union(post)

        except IndexError:
            return JsonResponse({
                'error': 'Not following anyone at the moment.'
                }, status = 400)
        
    # Returns a json response with all the posts ordered by the most recent showing up first
    return JsonResponse([post.serialize() for post in posts.order_by('-timestamp')], safe=False)


@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        post = Posts(
            owner = request.user,
            text = request.POST['new_post_text']
        )
        post.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseForbidden('This route only accepts POSTs')



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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
