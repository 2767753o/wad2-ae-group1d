from datetime import datetime, timedelta
import pytz # timezones

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.urls import reverse

from blink_app.forms import UserForm, UserProfileForm, CreateForm
from blink_app.models import Post, UserProfile, Like, Comment
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required
def index(request):
    # get all posts
    postData = Post.objects.order_by('-releaseDate')
    likeData = []
    userLikeData = []
    for post in postData:
        likeData.append(len(Like.objects.filter(post=post)))    
        userLikeData.append(len(Like.objects.filter(post=post).filter(user=request.user))>0)

    return render(
        request,
        'blink/index.html',
        context={
            'postAndLikeData': zip(postData, likeData, userLikeData)
        }
    )

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                # update posted by checking when user last posted
                user_data = User.objects.get(username=username)
                user_profile_data = UserProfile.objects.get(user=user_data)
                user_post_data = Post.objects.filter(user=user_data).order_by('-releaseDate')

                # check if user has posted in the last 24 hours
                utc = pytz.UTC
                if len(user_post_data) > 0 and user_post_data[0].releaseDate + timedelta(days=1) < utc.localize(datetime.now()):
                    user_profile_data.posted = False
                    user_profile_data.save()

                login(request, user)
                return redirect(reverse('blink:index'))
            else:
                return HttpResponse("Your account is disabled.")
            
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    
    else:
        return render(request, 'blink/login.html')

def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name='registration/password_reset_email.html',
                subject_template_name='registration/password_reset_subject.txt',
                from_email=None,
                html_email_template_name=None,
                extra_email_context=None,
            )
            return render(request, 'blink/reset_password_done.html')
    else:
        form = PasswordResetForm()
    return render(request, 'blink/reset_password.html', {'form': form})


def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profilePicture' in request.FILES:
                profile.profilePicture = request.FILES['profilePicture']

            profile.save()

            registered = True

        else:
            print(user_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(
        request,
        'blink/register.html',
        context={
            'user_form': user_form,
            'profile_form': profile_form,
            'registered': registered
        }
    )

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('blink:login'))

@login_required
def view_user(request, username):
    # get user data of user currently logged in
    try:
        userData = User.objects.get(username=username)
        userProfileData = UserProfile.objects.get(user=userData)
        postData = Post.objects.order_by('-releaseDate')
    except User.DoesNotExist:
        userData = None

    if userData is None:
        return redirect(reverse('blink:index'))

    return render(
        request, 'blink/user.html', 
        context={
            'userData': userData,
            'userProfileData': userProfileData,
            'postData': postData
        }
    )

@login_required
def create(request):
    if request.method == "POST":
        create_form = CreateForm(request.POST)

        # check if user has already posted
        try:
            user_data = User.objects.get(username=request.user.get_username())
            user_profile_data = UserProfile.objects.get(user=user_data)
        except User.DoesNotExist:
            user_data = None

        if user_data is None or user_profile_data.posted:
            return redirect(reverse('blink:index'))
        
        if create_form.is_valid():
            post_form = create_form.save(commit=False)

            if 'image' in request.FILES:
                post_form.image = request.FILES['image']

            post_form.releaseDate = datetime.now()
            post_form.user = user_data

            post_form.save()
            user_profile_data.posted = True
            user_profile_data.save()

            return redirect(reverse('blink:index')) 

        else:
            print(post_form.errors)

    else:
        post_form = CreateForm()

    return render(
        request,
        'blink/create.html',
        context={
            'post_form': post_form,
        }
    )

@login_required
def search(request):
    # search posts and users
    query = request.GET.get('search')
    if query != "":
        post_results = Post.objects.filter(Q(content__icontains=query)).order_by('-releaseDate')
        user_results = User.objects.filter(Q(username__icontains=query)).order_by('username')
        user_profile_results = UserProfile.objects.filter(Q(user__username__icontains=query)).order_by('user__username')
        user_data = zip(user_results, user_profile_results)

        return render(
            request,
            'blink/search.html',
            context={
                'post_results': post_results,
                'user_data': user_data,
                'query': query
            }
        )
    
    else:
        return redirect(reverse('blink:index'))

@login_required
def view_post(request, postID):
    try:
        postData = Post.objects.get(postID=postID)
        likeData = Like.objects.filter(post=postData).filter(user=request.user)
        likeCount = len(Like.objects.filter(post=postData))
    except Post.DoesNotExist:
        postData = None

    if postData is None:
        return redirect(reverse('blink:index'))

    return render(
        request, 'blink/post.html', 
        context={
            'postData': postData,
            'userLiked': len(likeData) > 0,
            'likeCount': likeCount
        }
    )

@login_required
def like_post(request, postID):
    try:
        postData = Post.objects.get(postID=postID)
        user_data = User.objects.get(username=request.user.get_username())
    except Post.DoesNotExist:
        postData = None
    except User.DoesNotExist:
        user_data = None

    if postData is None or user_data is None:
        return redirect(reverse('blink:index'))
    
    likeData = Like.objects.filter(post=postData).filter(user=user_data)
    if len(likeData) > 0:
        likeInstance = Like.objects.get(post=postData, user=user_data)
        likeInstance.delete()
    else:
        like = Like(user=user_data, post=postData)
        like.save()

    return redirect(request.META["HTTP_REFERER"])

@login_required
def view_likes(request, postID):
    try:
        postData = Post.objects.get(postID=postID)
        likeData = Like.objects.filter(post=postData)
    except Post.DoesNotExist:
        postData = None

    if postData is None:
        return redirect(reverse('blink:index'))
    
    return render(
        request, 'blink/likes.html',
        context={
            'postData': postData,
            'likeData': likeData
        }
    )

def friends(request):
    return render(request, 'blink/friends.html')

def settings(request):
    return render(request, 'blink/settings.html')

def about(request):
    return render(request, 'blink/about.html')

def help(request):
    return render(request, 'blink/help.html')

def user_analytics(request):
    return render(request, 'blink/analytics.html')

def user_followed_by(request):
    return render(request, 'blink/followed_by.html')

def user_following(request):
    return render(request, 'blink/following.html')