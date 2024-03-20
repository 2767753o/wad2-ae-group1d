from django.test import TestCase
from datetime import datetime, timedelta
from django.urls import reverse
from blink_app.models import Post, Like, Comment, User, Friendship
import pytz

class BlinkUnitTests(TestCase):
    """
    Tests to do with user authentication
    """
    def setUp(self):
        # Set up a test user
        self.user = User.objects.create_user(username='tester', email = 'test@fake.com', password = 'password')
        self.client.login(username = 'testuser', password = 'password')

    def test_userRegistation_and_login(self):
        response = self.client.post(reverse('blink:register'), {
            'username': 'newuser',
            'email': 'newuser@fake.com',
            'password1': 'newpassword',
            'password2': 'newpassword',
        })
        self.assertEqual(response.status_code, 302, )

        login = self.client.login(username='newuser', password='newpassword')
        self.assertTrue(login)

class BlinkPostTests(TestCase):
    """
    Tests to do with post creation, viewing and deletion
    """
    def setUp(self):
        # Set up a test user for posts
        self.user = User.objects.create_user(username='postuser', email = 'test@fake.com', password = 'password')
        self.client.login(username = 'postuser', password = 'password')
        
    def test_post_creation(self):
        response = self.client.post(reverse('blink:create'), {
            'content': 'Test post',
        })
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('blink:create'), {
            'content': 'This should not be possible',
        })
        self.assertNotEqual(response.status_code, 302)

    def testPostDeletion(self):
        deletion_post = Post.objects.create(
            user = self.user,
            content = 'this post is FINISHED',
            releaseDate = datetime.now(pytz.UTC) - timedelta(days = 1, minutes = 1)
        )
        
        self.client.get(reverse('blink:index'))
        self.assertFalse(Post.objects.filter(postID = deletion_post.id).exists())

class UserProfileTests(TestCase):
    """
    Tests for user profiles
    """
    def setUp(self):
        self.user = User.objects.create_user(username='viewUser', email = 'test@fake.com', password = 'password')
        self.client.login(username='viewUser', password='password')
    
    def test_profile_view(self):
        response = self.client.get(reverse('blink:user', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

class PostInteravtionTests(TestCase):
    """
    Tests for post interaction
    """
    def setUp(self):
        self.user = User.objects.create_user(username='interactUser', email = 'test@fake.com', password = 'password')
        self.client.login(username='interactUser', password='password')
        self.post = Post.objects.create(
            user=self.user, 
            content="Interact with this!")
        
    def test_like_post(self):
        self.client.get(reverse('blink:like_post', kwargs={'postID': self.post.postID}))
        self.assertTrue(Like.objects.filter(user=self.user, post=self.post).exists)

    def test_comment_post(self):
        self.client.post(reverse('blink:comment', kwargs={'postID': self.post.postID}), {'comment': 'Test comment'})
        self.assertTrue(Comment.objects.filter(user=self.user, post=self.post, content='Test comment').exists)

class FreindshipTests(TestCase):
    """
    Tests for friendship
    """
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', email = 'user1@fake.com', password = 'friend1')
        self.user2 = User.objects.create_user(username='user2', email = 'user2@fake.com', password = 'friend2')
        self.client.login(username='user1', password='friend1')
    
    def test_create_friendship(self):
        Friendship.objects.create(user=self.user1, friend=self.user2)
        self.assertTrue(Friendship.objects.filter(user=self.user1, friend=self.user2).exists())