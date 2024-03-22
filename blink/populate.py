import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blink.settings")

import django
django.setup()
from blink_app.models import Post, UserProfile, Comment, Like, Friendship
from django.contrib.auth.models import User

import json
import datetime
import random
random.seed(413)


def addUser(username, password, firstName, lastName, emailAddress, profilePicture, isStaff=False):
    user = User.objects.create_user(
        username = username,
        first_name = firstName,
        last_name = lastName,
        password = password,
        email = emailAddress,
    )
    user.is_staff = isStaff
    user.is_superuser = isStaff
    user.save()
    userProfile = UserProfile.objects.get_or_create(
        user = user,
        profilePicture = profilePicture
    )[0]
    userProfile.save()
    return userProfile


def addPost(hoursAgo, content, image, username):
    user = User.objects.get(username=username)
    post = Post.objects.get_or_create(
        releaseDate = datetime.datetime.now() - datetime.timedelta(hours=hoursAgo),
        content = content,
        image = image,
        user = user
    )[0]
    post.save()
    return post


def addComment(content, username, poster, hoursAgo):
    commentTime = datetime.datetime.now() - datetime.timedelta(hours=hoursAgo)
    user = User.objects.get(username=username)
    poster = User.objects.get(username=poster)
    post = Post.objects.get(user=poster)
    comment = Comment.objects.get_or_create(
        commentTime = commentTime,
        content = content,
        user = user,
        post = post
    )[0]
    comment.save()
    return comment


def addLike(username, poster, commentContent):
    user = User.objects.get(username=username)
    if commentContent:
        comment = Comment.objects.filter(content=commentContent)[0]
        like = Like.objects.get_or_create(
            user = user,
            comment = comment
        )[0]
    elif poster:
        poster = User.objects.filter(username=poster)[0]
        post = Post.objects.filter(user=poster)[0]
        like = Like.objects.get_or_create(
            user = user,
            post = post
        )[0]
    else:
        quit("No content provided for like")
    
    like.save()
    return like


def addFriendship(username, friendname):
    user = User.objects.get(username=username)
    friend = User.objects.get(username=friendname)
    friendship = Friendship.objects.get_or_create(
        user = user,
        friend = friend
    )[0]
    friendship.save()
    return friendship


def getData():
    with open("populationData/users.json") as f:
        users = json.load(f)

    with open("populationData/posts.json") as f:
        posts = json.load(f)

    with open("populationData/comments.json") as f:
        comments = json.load(f)

    with open("populationData/likes.json") as f:
        likes = json.load(f)

    with open("populationData/friendships.json") as f:
        friendships = json.load(f)

    return users, posts, comments, likes, friendships


def populate(users, posts, comments, likes, friendships):
    for user in users:
        addUser(
            user['username'],
            user['password'],
            user['firstName'],
            user['lastName'],
            user['emailAddress'],
            user['profilePicture'],
            user['isStaff']
        )

    for post in posts:
        addPost(
            post['hoursAgo'],
            post['content'],
            post['image'],
            post['username']
        )

    for comment in comments:
        addComment(
            comment['content'],
            comment['username'],
            comment['poster'],
            comment['hoursAgo']
        )

    for like in likes:
        addLike(
            like['username'],
            like['poster'],
            like['commentContent']
        )

    for friendship in friendships:
        addFriendship(
            friendship['username'],
            friendship['friendname']
        )


def printResults():
    print(f"Users: {len(User.objects.all())}")
    print(f"Posts: {len(Post.objects.all())}")
    print(f"Comments: {len(Comment.objects.all())}")
    print(f"Likes: {len(Like.objects.all())}")
    print(f"Friendships: {len(Friendship.objects.all())}")


def main():
    users, posts, comments, likes, friendships = getData()
    populate(users, posts, comments, likes, friendships)
    printResults()


if __name__ == '__main__':
    main()