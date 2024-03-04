from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import redirect
from django.urls import reverse


def index(request):
    return render(request, 'blink/index.html')

def login(request):
    return render(request, 'blink/login.html')

def resetPassword(request):
    return render(request, 'blink/resetPassword.html')

def register(request):
    return render(request, 'blink/register.html')

def friends(request):
    return render(request, 'blink/friends.html')

def view_post(request):
    return render(request, 'blink/post.html')

def view_likes(request):
    return render(request, 'blink/likes.html')

def search(request):
    return render(request, 'blink/search.html')

def create(request):
    return render(request, 'blink/create.html')

def settings(request):
    return render(request, 'blink/settings.html')

def about(request):
    return render(request, 'blink/about.html')

def help(request):
    return render(request, 'blink/help.html')

def view_user(request):
    return render(request, 'blink/user.html')

def user_analytics(request):
    return render(request, 'blink/analytics.html')

def user_followed_by(request):
    return render(request, 'blink/followed_by.html')

def user_following(request):
    return render(request, 'blink/following.html')

def user_logout(request):
    return render(request, 'blink/logout.html')