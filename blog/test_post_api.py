from datetime import datetime
from pytz import UTC

# Django 
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

# Models
from blog.models import Post

# Class Test
class PostApiTestCase(TestCase):
  
  # Setup data for all tests
  def setUp(self):
    # Two Test Users
    self.u1 = get_user_model().objects.create(
      email="user1@gmail.com",
      password="1234",
    )

    self.u2 = get_user_model().objects.create(
      email="user2@gmail.com",
      password="1234",
    )

    # Two Test Posts
    _ = 1
    p1 = Post.objects.create(
        title=f"Post {_}",
        published_at=timezone.now(),
        slug=f"Post {_}",
        summary=f"Summary for Post {_}",
        content=f"Content for Post {_}",
        author=self.u1
    )

    _ = 2
    p2 = Post.objects.create(
        title=f"Post {_}",
        published_at=timezone.now(),
        slug=f"Post {_}",
        summary=f"Summary for Post {_}",
        content=f"Content for Post {_}",
        author=self.u2
    )

    self.post_lookup = {
      p1.id : p1,
      p2.id : p2,
    }

    # Use APIClient
    self.client = APIClient()

    # Create Token
    self.t1 = Token.object.create(user=self.u1)
    self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.t1.key}")


    # Test Post List
    def test_post_list(self):
      resp = self.client.get("/api/v1/posts/")
      data = resp.json()
      self.assertEqual(len(posts), 2)

      for post_dict in data:
          post_obj = self.post_lookup[post_dict["id"]]
          self.assertEqual(post_obj.title, post_dict["title"])
          self.assertEqual(post_obj.slug, post_dict["slug"])
          self.assertEqual(post_obj.summary, post_dict["summary"])
          self.assertEqual(post_obj.content, post_dict["content"])
          self.assertTrue(
              post_dict["author"].endswith(f"/api/v1/users/{post_obj.author.email}")
          )
          self.assertEqual(
              post_obj.published_at,
              datetime.strptime(
                  post_dict["published_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
              ).replace(tzinfo=UTC),
          )
    
    # Test Create Post with no Authentication
    def test_unauthenticated_post_create(self):

      # Logout current client
      self.client.credentials()

      post_dict = {
          "title": "Test Post",
          "slug": "test-post-3",
          "summary": "Test Summary",
          "content": "Test Content",
          "author": "http://testserver/api/v1/users/test@example.com",
          "published_at": "2021-01-10T09:00:00Z",
      }

      # Send Request
      resp = self.client.post("/api/v1/posts")
      self.assertEqual(resp.status_code, 401)
      self.assertEqual(Post.objects.all().count(), 2)


    # Test Create Post as Authenticated
    def test_post_create(self):

      post_dict = {
          "title": "Test Post",
          "slug": "test-post-3",
          "summary": "Test Summary",
          "content": "Test Content",
          "author": "http://testserver/api/v1/users/test@example.com",
          "published_at": "2021-01-10T09:00:00Z",
      }

      # Send Request
      resp = self.client.post("/api/v1/posts")
      self.assertEqual(resp.status_code, 302)
      self.assertEqual(Post.objects.all().count(), 3)

      # Match Data
      post_id = resp.json()["id"]
      created_post = Post.objects.get(pk=post_id)
      self.assertEqual(post_dict['title'], created_post.title)
      self.assertEqual(post_dict['slug'], created_post.slug)
      self.assertEqual(post_dict['summary'], created_post.summary)
      self.assertEqual(post_dict['content'], created_post.content)
      self.assertEqual(post_dict['published_at'], datetime(2021, 1, 10, 9, 0, 0, tzinfo=UTC))
      self.assertEqual(post_dict['author'], self.u1)

      

