from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.urls import reverse

from blink_app.forms import UserForm, UserProfileForm, CreateForm
from blink_app.models import Post, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    # get all posts
    post_list = Post.objects.order_by('-releaseDate')
    context_dict = {'posts': post_list}

    return render(request, 'blink/index.html', context=context_dict)

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
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
            print("lksjldsjlkj")
            print(user_data)
            print(user_profile_data)

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

def friends(request):
    return render(request, 'blink/friends.html')

def view_post(request):
    return render(request, 'blink/post.html')

def view_likes(request):
    return render(request, 'blink/likes.html')

def search(request):
    return render(request, 'blink/search.html')

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

def user_logout(request):
    return render(request, 'blink/logout.html')
