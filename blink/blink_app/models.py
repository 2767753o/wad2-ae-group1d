from django.db import models

class Post(models.Model):
    PostID = models.AutoField(primary_key=True)
    ReleaseDate = models.DateTimeField()
    Views = models.IntegerField(default=0)
    Content = models.CharField(max_length=280)
    HasImages = models.BooleanField(default=False)
    Image = models.ImageField(upload_to='post_images', null=True, blank=True)

class User(models.Model):
    UserID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=128)
    Posted = models.BooleanField(default=False)

class Comment(models.Model):
    CommentID = models.AutoField(primary_key=True)
    CommentTime = models.DateTimeField()
    Content = models.CharField(max_length=280)

class Like(models.Model):
    LikeID = models.CharField(primary_key=True, max_length=8)

