from django.test import TestCase
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.urls import reverse
from blink_app.models import Post
import pytz
import os

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

f"{FAILURE_HEADER} {FAILURE_FOOTER}"


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
        self.assertEqual(response.status_code, 302)

        login = self.client.login(username='newuser', password='newpassword')
        self.assertTrue(login)

class BlinkPostTests(TestCase):
    """
    Tests to do with post creation, viewing and deletion
    """
    def setUp(self):
        # Set up a test user
        self.user = User.objects.create_user(username='tester', email = 'test@fake.com', password = 'password')
        self.client.login(username = 'testuser', password = 'password')
        
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
        self.assertFalse(Post.objects.filter(postId = deletion_post.id).exists())