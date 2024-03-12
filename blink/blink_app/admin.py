from django.contrib import admin
from blink_app.models import Post, UserProfile, Comment, Like, Friendship

admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Friendship)
