from datetime import datetime
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Post(models.Model):
    release_date = models.DateTimeField(default=datetime.now)
    content = models.CharField(max_length=280)
    image = models.ImageField(upload_to='post_pictures', null=True, blank=True)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    posted = models.BooleanField(default=False)
    profilePicture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        if not self.username_slug:
            self.username_slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)
    
class Comment(models.Model):
    commentTime = models.DateTimeField()
    content = models.CharField(max_length=280)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    post = models.ForeignKey(Post, on_delete= models.CASCADE)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    post = models.ForeignKey(Post, on_delete= models.CASCADE, null = True, blank = True)
    comment = models.ForeignKey(Comment, on_delete= models.CASCADE, null = True, blank = True)

class Friendship(models.Model):
    user = models.ForeignKey(User, related_name= 'friends_of', on_delete= models.CASCADE)
    friend = models.ForeignKey(User, related_name= 'friends', on_delete= models.CASCADE)
