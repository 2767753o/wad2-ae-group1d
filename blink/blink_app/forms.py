from django import forms
from django.contrib.auth.models import User
from blink_app.models import UserProfile, Post


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profilePicture',)


class CreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content', 'image',)