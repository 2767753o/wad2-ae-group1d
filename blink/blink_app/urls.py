from django.urls import path
from blink_app import views
from django.contrib.auth import views as auth_views

app_name = 'blink'

urlpatterns = [
        path('', views.index, name='index'),
        path('login/', views.user_login, name='login'),
        path('reset_password/', views.reset_password, name='reset_password'),
        path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='reset_password_done'),
        path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
        path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(), name='reset_password_complete'),
        path('register/', views.register, name='register'),
        path('friends/', views.friends, name='friends'),
        # path('post/<id:postId>/', views.view_post, name='view_post'),
        # path('post/<id:postId>/likes', views.view_likes, name='view_likes'),
        path('search/', views.search, name='search'),
        path('create/', views.create, name='create'),
        path('settings/', views.settings, name='settings'),
        path('about/', views.about, name='about'),
        path('help/', views.help, name='help'),
        path('user/<str:username>/', views.view_user, name='user'),
        # path('user/<id:userId>/settings', views.user_settings, name='user_settings'),
        # path('user/<id:userId>/analytics', views.user_analytics, name='user_analytics'),
        # path('user/<id:userId>/followed', views.user_followed_by, name='user_followed_by'),
        # path('user/<id:userId>/following', views.user_following, name='user_following'),
        path('logout/', views.user_logout, name='logout'),
]
