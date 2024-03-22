from datetime import datetime
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Post(models.Model):
    postID = models.AutoField(primary_key=True)
    releaseDate = models.DateTimeField(default=datetime.now)
    views = models.IntegerField(default=0)
    content = models.CharField(max_length=280)
    image = models.ImageField(upload_to='post_pictures', null=True, blank=True)
    user = models.ForeignKey(User, on_delete= models.CASCADE)

class UserProfile(models.Model):
    userID = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    posted = models.BooleanField(default=False)
    profilePicture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    commentID = models.AutoField(primary_key=True)
    commentTime = models.DateTimeField()
    content = models.CharField(max_length=280)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    post = models.ForeignKey(Post, on_delete= models.CASCADE)

class Like(models.Model):
    likeID = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    post = models.ForeignKey(Post, on_delete= models.CASCADE, null = True, blank = True)
    comment = models.ForeignKey(Comment, on_delete= models.CASCADE, null = True, blank = True)

class Friendship(models.Model):
    user = models.ForeignKey(User, related_name= 'friends_of', on_delete= models.CASCADE)
    friend = models.ForeignKey(User, related_name= 'friends', on_delete= models.CASCADE)
    class Meta:
        unique_together = ('user', 'friend')