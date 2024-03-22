from django.test import TestCase
from datetime import datetime, timedelta
from django.urls import reverse
from blink_app.models import Post, Like, Comment, User, Friendship, UserProfile
import pytz

class BlinkUserTests(TestCase):
    """
    Tests to do with user authentication
    """
    def test_user_registation(self):
        """
        Tests to check user registration and then login
        """
        response = self.client.post(reverse('blink:register'), {
            'username': 'newuser',
            'email': 'newuser@fake.com',
            'password1': 'newpassword',
            'password2': 'newpassword',
        })
        self.assertEqual(response.status_code, 200)

    def test_user_login(self):
        self.user = User.objects.create_user(username='newuser', email = 'test@fake.com', password = 'newpassword')
        UserProfile.objects.create(user=self.user)

        login = self.client.login(username='newuser', password='newpassword')
        self.assertTrue(login)

    def test_user_logout(self):
        """
        Tests to check the user has logged out
        """
        self.client.login(username='newuser', password='newpassword')
        self.client.logout()
        response = self.client.get(reverse('blink:index'))
        self.assertNotEqual(response.status_code, 403)

class BlinkPostTests(TestCase):
    """
    Tests to do with post creation, viewing and deletion
    """
    def setUp(self):
        # Set up a test user for posts
        self.user = User.objects.create_user(username='postuser', email = 'test@fake.com', password = 'password')
        UserProfile.objects.create(user=self.user)
        self.client.login(username = 'postuser', password = 'password')
        
    def test_post_creation(self):
        """
        Tests what happens when a post is created and also that a user cannot post a second time.
        """
         
        response = self.client.post(reverse('blink:create'), {
            'content': 'Test post',
        })
        self.assertEqual(response.status_code, 302)

        inital_post_count = Post.objects.filter(user=self.user).count()

        response = self.client.post(reverse('blink:create'), {
            'content': 'This should not be possible',
        })

        self.assertEqual(response.status_code, 302)

        new_post_count = Post.objects.filter(user=self.user).count()
        self.assertEqual(new_post_count, inital_post_count)
    def testPostDeletionIn24Hour(self):
        """
        Test to check the post has been deleted after 1 day
        """
        deletion_post = Post.objects.create(
            user = self.user,
            content = 'this post is FINISHED',
            releaseDate = datetime.now(pytz.UTC) - timedelta(days = 1, minutes = 1)
        )
        
        self.client.get(reverse('blink:index'))
        self.assertFalse(Post.objects.filter(id = deletion_post.id).exists())

class UserProfileTests(TestCase):
    """
    Tests for user profiles
    """
    def setUp(self):
        self.user = User.objects.create_user(username='viewUser', email = 'test@fake.com', password = 'password')
        UserProfile.objects.create(user=self.user)
        self.client.login(username='viewUser', password='password')
    
    def test_profile_view(self):
        """
        Tests to check profile view
        """
        response = self.client.get(reverse('blink:user', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

class PostInteractionTests(TestCase):
    """
    Tests for post interaction
    """
    def setUp(self):
        self.user = User.objects.create_user(username='interactUser', email = 'test@fake.com', password = 'password')
        UserProfile.objects.create(user=self.user)
        self.client.login(username='interactUser', password='password')

        self.post = Post.objects.create(
            user=self.user, 
            content="Interact with this!")
        
        #creates new comment
        self.comment = Comment.objects.create(
            user = self.user,
            post = self.post, 
            content = "Like this!",
            commentTime = datetime.now(pytz.UTC)
        )

    def test_like_post(self):
        """
        Test to check post likes exist
        """
        self.like = Like.objects.create(
            user = self.user,
            post = self.post
        )
        self.assertTrue(Like.objects.filter(user=self.user, post=self.post).exists())

    def test_ensure_likes_go_up(self):
        """
        Tests to check post likes go up when liked
        """
        initial_likes = Like.objects.filter(post=self.post).count()

        self.like = Like.objects.create(
            user = self.user,
            post = self.post
        )

        new_likes = Like.objects.filter(post=self.post).count()
        self.assertEqual(new_likes, initial_likes + 1)

    def test_ensure_comments_go_up(self):
        """
        Tests to check a comment has been entered
        """
        comment_count = Comment.objects.filter(post=self.post).count()

        self.secondcomment = Comment.objects.create(
            user = self.user,
            post = self.post, 
            content = "Like this!",
            commentTime = datetime.now(pytz.UTC)
        )

        new_comment_count = Comment.objects.filter(post=self.post).count()
        self.assertEqual(new_comment_count, comment_count + 1)

    def test_comment_likes(self):
        """
        Tests to check a comments likes go up when comment is liked
        """
        initial_likes = Like.objects.filter(comment=self.comment).count()
        self.like = Like.objects.create(
            user = self.user,
            comment = self.comment
        )
        new_likes = Like.objects.filter(comment=self.comment).count()
        self.assertEqual(new_likes, initial_likes + 1)

    def test_comment_exist(self):
        """
        Test to check post comments exist
        """
        self.assertTrue(Comment.objects.filter(user=self.user, post=self.post, content='Like this!').exists())

class FreindshipTests(TestCase):
    """
    Tests for friendship
    """
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', email = 'user1@fake.com', password = 'friend1')
        UserProfile.objects.create(user=self.user1)

        self.user2 = User.objects.create_user(username='user2', email = 'user2@fake.com', password = 'friend2')
        UserProfile.objects.create(user=self.user2)

        self.client.login(username='user1', password='friend1')
        
    def test_create_friendship(self):
        Friendship.objects.create(user=self.user1, friend=self.user2)
        self.assertTrue(Friendship.objects.filter(user=self.user1, friend=self.user2).exists())

