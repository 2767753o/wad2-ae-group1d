from django.urls import path
from blink_app import views
from django.contrib.auth import views as auth_views

app_name = 'blink'

urlpatterns = [
        path('', views.index, name='index'),
        path('login/', views.user_login, name='login'),
        path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
        path('register/', views.register, name='register'),
        path('friends/', views.friends, name='friends'),
        path('post/<int:postID>/', views.view_post, name='view_post'),
        path("like_post/", views.LikePostView.as_view(), name="like_post"),
        path('post/<int:postID>/likes', views.view_likes_post, name='view_likes_post'),
        path('post/<int:postID>/comment', views.comment, name='comment'),
        path('like_comment/', views.LikeCommentView.as_view(), name='like_comment'),
        path('comment/<int:commentID>/likes', views.view_likes_comment, name='view_likes_comment'),
        path('search/', views.SearchView.as_view(), name='search'),
        path('create/', views.create, name='create'),
        path('about/', views.about, name='about'),
        path('help/', views.help, name='help'),
        path('user/<str:username>/', views.view_user, name='user'),
        path('delete_post/', views.DeletePostView.as_view(), name='delete_post'),
        path('logout/', views.user_logout, name='logout'),
        path('follow/', views.followed, name='follow'),
        path('user/<int:user_id>/following/', views.user_following, name='user_following'),
        path('user/<int:user_id>/followed/', views.user_followed, name='user_followed'),
        path('following/', views.following, name='following'),
        path('user/<int:user_id>/toggle_follow/', views.toggle_follow, name='toggle_follow'),
]

