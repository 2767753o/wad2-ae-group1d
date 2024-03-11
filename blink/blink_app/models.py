from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    postID = models.AutoField(primary_key=True)
    releaseDate = models.DateTimeField()
    views = models.IntegerField(default=0)
    content = models.CharField(max_length=280)
    hasImages = models.BooleanField(default=False)
    image = models.ImageField(upload_to='post_images', null=True, blank=True)
    user = models.ForeignKey(User, on_delete= models.CASCADE)

class User(models.Model):
    userID = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    posted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
    
class Comment(models.Model):
    commentID = models.AutoField(primary_key=True)
    commentTime = models.DateTimeField()
    content = models.CharField(max_length=280)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    post = models.ForeignKey(Post, on_delete= models.CASCADE)

class Like(models.Model):
    likeID = models.CharField(primary_key=True, max_length=8)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    post = models.ForeignKey(Post, on_delete= models.CASCADE, null = True, blank = True)
    comment = models.ForeignKey(Comment, on_delete= models.CASCADE, null = True, blank = True)
    