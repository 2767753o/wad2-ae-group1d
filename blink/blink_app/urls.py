from django.urls import path
from blink_app import views

app_name = 'blink'

urlpatterns = [
        path('', views.index, name='index'),
        path('login/', views.login, name='login'),
        path('resetPassword/', views.resetPassword, name='resetPassword'),
        path('register/', views.register, name='register'),
        path('friends/', views.friends, name='friends'),
        # path('post/<id:postId>/', views.view_post, name='view_post'),
        # path('post/<id:postId>/likes', views.view_likes, name='view_likes'),
        path('search/', views.search, name='search'),
        path('create/', views.create, name='create'),
        path('settings/', views.settings, name='settings'),
        path('about/', views.about, name='about'),
        path('help/', views.help, name='help'),
        # path('user/<id:userId>/', views.view_user, name='view_user'),
        # path('user/<id:userId>/settings', views.user_settings, name='user_settings'),
        # path('user/<id:userId>/analytics', views.user_analytics, name='user_analytics'),
        # path('user/<id:userId>/followed', views.user_followed_by, name='user_followed_by'),
        # path('user/<id:userId>/following', views.user_following, name='user_following'),
        path('logout/', views.user_logout, name='logout'),
]
