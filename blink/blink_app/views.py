from datetime import datetime, timedelta
from django.views import View
from django.utils.decorators import method_decorator
import pytz # timezones

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

from blink_app.forms import UserForm, UserProfileForm, CreateForm
from blink_app.models import Post, UserProfile, Like, Comment
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import User, Friendship


def get_time_posted(utc, releaseDate):
    seconds = (utc.localize(datetime.now()) - releaseDate).seconds
    if seconds // 3600 > 0:
        res = f"{seconds // 3600} hour"
        if seconds // 3600 != 1:
            res += "s"
    elif seconds // 60 > 0:
        res = f"{seconds // 60} minute"
        if seconds // 60 != 1:
            res += "s"
    else:
        res = f"{seconds} second"
        if seconds != 1:
            res += "s"

    return res + " ago"


@login_required
def index(request):
    # get all posts
    postData = Post.objects.order_by('-releaseDate')
    likeData = []
    userLikeData = []
    timePosted = []
    userProfileData = []
    for post in postData:
        # check if post is within 24h
        utc = pytz.UTC
        if post.releaseDate + timedelta(days=1) < utc.localize(datetime.now()):
            post.delete()
        else:
            likeData.append(len(Like.objects.filter(post=post)))    
            userLikeData.append(len(Like.objects.filter(post=post).filter(user=request.user))>0)
            timePosted.append(get_time_posted(utc, post.releaseDate))
            userProfileData.append(UserProfile.objects.get(user=post.user))

    return render(
        request,
        'blink/index.html',
        context={
            'data': zip(postData, likeData, userLikeData, timePosted, userProfileData)
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
                if (len(user_post_data) > 0 and user_post_data[0].releaseDate + timedelta(days=1) < utc.localize(datetime.now())) or len(user_post_data) == 0:
                    user_profile_data.posted = False
                    user_profile_data.save()

                login(request, user)
                messages.success(request, f'You are now successfully logged in.')
                return redirect(reverse('blink:index'))
            else:
                messages.error(request, f'This account is disabled.')
                return redirect(reverse('blink:login'))
            
        else:
            messages.error(request, f'Invalid login details supplied.')
            return redirect(reverse('blink:login'))
    
    else:
        return render(request, 'blink/login.html')


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
def view_user(request, username_slug):
    page_user = get_object_or_404(User, slug=username_slug)
    is_self_page = request.user == page_user
    is_following = Friendship.objects.filter(user=request.user, friend=page_user).exists()
    # get user data of user currently logged in
    following_count = Friendship.objects.filter(user=page_user).count()
    followers_count = Friendship.objects.filter(friend=page_user).count()
    try:
        userData = User.objects.get(username=username_slug)
        userProfileData = UserProfile.objects.get(user=userData)
    except User.DoesNotExist:
        userData = None
        userProfileData = None
    
    try:
        postData = Post.objects.get(user=userData)
        timePosted = get_time_posted(pytz.UTC, postData.releaseDate)
    except Post.DoesNotExist:
        postData = None
        timePosted = None

    if userData is None:
        return redirect(reverse('blink:index'))

    return render(
        request, 'blink/user.html', 
        context={
            'userData': userData,
            'userProfileData': userProfileData,
            'postData': postData,
            'timePosted': timePosted,
            'page_user': page_user,
            'is_self_page': is_self_page,
            'is_following': is_following,
            'following_count': following_count,
            'followers_count': followers_count,
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
def view_post(request, post_id):
    try:
        postData = Post.objects.get(id=post_id)
        userProfile = UserProfile.objects.get(user=postData.user)
        commentData = Comment.objects.filter(post=postData).order_by('commentTime')
        likeData = Like.objects.filter(post=postData).filter(user=request.user)
        
        likeDataComments = [
            len(Like.objects.filter(comment=comment)) for comment in commentData
        ]
        userLikedComments = [
            len(Like.objects.filter(comment=comment).filter(user=request.user)) > 0 for comment in commentData
        ]
        userProfileComments = [
            UserProfile.objects.get(user=comment.user) for comment in commentData
        ]
        
        likeCount = len(Like.objects.filter(post=postData))
    except Post.DoesNotExist:
        postData = None

    if postData is None:
        return redirect(reverse('blink:index'))
    
    timePosted = get_time_posted(pytz.UTC, postData.releaseDate)

    return render(
        request, 'blink/post.html', 
        context={
            'postData': postData,
            'userProfile': userProfile,
            'commentData': zip(commentData, likeDataComments, userLikedComments, userProfileComments),
            'userLiked': len(likeData) > 0,
            'likeCount': likeCount,
            'timePosted': timePosted,
        }
    )

@login_required
def view_likes_post(request, post_id):
    try:
        postData = Post.objects.get(id=post_id)
        likeData = Like.objects.filter(post=postData)
    except Post.DoesNotExist:
        postData = None

    if postData is None:
        return redirect(reverse('blink:index'))
    
    return render(
        request, 'blink/likes.html',
        context={
            'postData': postData,
            'likeData': likeData,
        }
    )

@login_required
def view_likes_comment(request, comment_id):
    try:
        commentData = Comment.objects.get(id=comment_id)
        likeData = Like.objects.filter(comment=commentData)
    except Comment.DoesNotExist:
        commentData = None

    if commentData is None:
        return redirect(reverse('blink:index'))
    
    return render(
        request, 'blink/likes.html',
        context={
            'commentData': commentData,
            'likeData': likeData,
            'post_id': commentData.post.id
        }
    )

@login_required
def comment(request, post_id):
    try:
        postData = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        postData = None

    if postData is None:
        return redirect(reverse('blink:index'))

    if request.method == "POST":
        comment = request.POST.get('comment')
        if len(comment) > 0:
            # comment must be non-empty
            userData = User.objects.get(username=request.user.get_username())
            commentInstance = Comment(user=userData, post=postData, content=comment)
            commentInstance.save()
        
    return redirect(reverse('blink:view_post', args=(id, )))

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


class LikeView(View):
    def getModel(self, post_id=None, comment_id=None):
        if post_id:
            try:
                return Post.objects.get(id=post_id)
            except Post.DoesNotExist:
                return None
            except ValueError:
                return None
            
        elif comment_id:
            try:
                return Comment.objects.get(id=comment_id)
            except Comment.DoesNotExist:
                return None
            except ValueError:
                return None
            
    def processLike(self, request, post=None, comment=None):
        userData = User.objects.get(username=request.user.get_username())
        if post:
            likeData = Like.objects.filter(post=post).filter(user=userData)
        elif comment:
            likeData = Like.objects.filter(comment=comment).filter(user=userData)

        if len(likeData) > 0:
            likeInstance = Like.objects.get(post=post, user=userData) if post else Like.objects.get(comment=comment, user=userData)
            likeInstance.delete()
            userLiked = "F"
        else:
            like = Like(user=userData, post=post) if post else Like(user=userData, comment=comment)
            like.save()
            userLiked = "T"

        numLikes = len(Like.objects.filter(post=post)) if post else len(Like.objects.filter(comment=comment))
        if numLikes != 1:
            plural = "T"
        else:
            plural = "F"

        # passed as strings to HttpResponse, so better to not do bool
        return numLikes, userLiked, plural


class LikePostView(LikeView):
    @method_decorator(login_required)
    def get(self, request):
        post_id = request.GET['post_id']
        post = self.getModel(id=post_id)
        if post is None:
            return HttpResponse(reverse('blink:index'))
        likeCount, userLiked, plural = self.processLike(request, post=post)
        return HttpResponse((userLiked, plural, likeCount))
    

class LikeCommentView(LikeView):
    @method_decorator(login_required)
    def get(self, request):
        comment_id = request.GET['comment_id']
        comment = self.getModel(id=comment_id)
        post = Post.objects.get(id=comment.post.id)
        if comment is None:
            return HttpResponse(reverse('blink:view_post', args=(post.id,)))
        likeCount, userLiked, plural = self.processLike(request, comment=comment)
        return HttpResponse((userLiked, plural, likeCount))
    

class SearchView(View):
    @method_decorator(login_required)
    def get(self, request):
        query = request.GET['search_query']
        post_results = Post.objects.filter(Q(content__icontains=query)).order_by('-releaseDate')

        post_data = post_results
        like_data = [len(Like.objects.filter(post=post)) for post in post_data]
        user_like_data = [len(Like.objects.filter(post=post).filter(user=request.user)) > 0 for post in post_data]
        timePosted = [get_time_posted(pytz.UTC, post.releaseDate) for post in post_data]
        userProfileData = [UserProfile.objects.get(user=post.user) for post in post_data]

        if query != "":
            user_results = User.objects.filter(Q(username__icontains=query)).order_by('username')
            user_profile_results = UserProfile.objects.filter(Q(user__username__icontains=query)).order_by('user__username')
            user_data = zip(user_results, user_profile_results)
        else:
            user_data = None

        title = "Search results for: " + query if query != "" else "BLINK"

        return render(
            request,
            "blink/search.html",
            context={
                'post_results': zip(post_data, like_data, user_like_data, timePosted, userProfileData),
                'user_data': user_data,
                'title': title,
                'query': query
            }
        )

def user_following(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    following = Friendship.objects.filter(user=user).select_related('friend')
    userProfileData = [
        UserProfile.objects.get(user=f.friend) for f in following
    ]
    return render(request, 'blink/follow.html', {
        'follows': zip(following, userProfileData), 
        'user': user
    })

def user_followed(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    followers = Friendship.objects.filter(friend=user)
    userProfileData = [
        UserProfile.objects.get(user=f.user) for f in followers
    ]

    return render(request, 'blink/followed.html', {
        'followers': zip(followers, userProfileData), 
        'user': user
    })

def followed(request, user_id):
    friend = get_object_or_404(User, pk=user_id)
    if Friendship.objects.filter(user=request.user, friend=friend).exists():
        return redirect('some-view-name')
    else:
        Friendship.objects.create(user=request.user, friend=friend)
        return redirect('some-view-name')

def following(request):
    following_ids = request.user.friends_of.values_list('friend_id', flat=True)
    posts = Post.objects.filter(user__in=following_ids).order_by('-releaseDate')
    
    likeData = []
    userLikeData = []
    timePosted = []
    userProfileData = []

    for post in posts:
        likeData.append(len(Like.objects.filter(post=post)))    
        userLikeData.append(len(Like.objects.filter(post=post).filter(user=request.user))>0)
        timePosted.append(get_time_posted(pytz.UTC, post.releaseDate))
        userProfileData.append(UserProfile.objects.get(user=post.user))

    return render(request, 'blink/following.html', {
        'data': zip(posts, likeData, userLikeData, timePosted, userProfileData)
    })

@require_POST
def toggle_follow(request, user_id):
    user_to_follow = get_object_or_404(User, pk=user_id)
    if Friendship.objects.filter(user=request.user, friend=user_to_follow).exists():
        Friendship.objects.filter(user=request.user, friend=user_to_follow).delete()
        followed = False
    else:
        Friendship.objects.create(user=request.user, friend=user_to_follow)
        followed = True
    # Redirect to the profile page of the user who was followed or unfollowed
    return redirect('blink:user', username=user_to_follow.username)



class DeletePostView(View):
    @method_decorator(login_required)
    def get(self, request):
        post_id = request.GET['post_id']
        try:
            post = Post.objects.get(id=post_id)
            user = post.user
            userProfile = UserProfile.objects.get(user=user)
            userProfile.posted = False
            post.delete()
            userProfile.save()
            
        # do nothing if error, redirect back to index
        except Post.DoesNotExist:
            pass
        except ValueError:
            pass

        return HttpResponse(reverse('blink:index'))
        