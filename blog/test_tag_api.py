# Django test
from django.test import LiveServerTestCase
from rest_framework.test import RequestsClient
from django.contrib.auth import get_user_model

# Models
from blog.models import Tag

# Requests Lib
from requests.auth import HTTPBasicAuth

class TagApiTestCase(LiveServerTestCase):
  
  def setUp(self):
    # Create User
    get_user_model().objects.create_user(
      email="admin@codio.com",
      password="1234"
    )

    # Tag urls
    self.url = self.live_server_url + "/api/v1/tags/"

    # tags
    self.tags = {
      "tag1",
      "tag2",
      "tag3",
      "tag4",
    }

    for tag in self.tags:
      Tag.objects.create(value=tag)

    # override client
    self.client = RequestsClient()

  def test_tag_list(self):
    resp = self.client.get(self.url)

    # Check Status
    self.assertEqual(resp.status_code, 200)
    # Check Values
    tags = resp.json()['results']
    print(tags)
    self.assertEqual({tag['value'] for tag in tags}, self.tags)
    
  def test_tag_create_token_auth(self):
    # Authenticate User
    resp = self.client.post(f"{self.live_server_url}/api/v1/token-auth/", {
      "username" : "admin@codio.com",
      "password" : "1234"
    })
    auth_token = resp.json()['token']
    self.client.headers['Authorization'] = f"Token {auth_token}"

    # Create Tag
    resp = self.client.post(self.url, {
      "value" : "tag5"
    })

    # Check Status
    self.assertEqual(resp.status_code, 201)
    # Check Tag
    tag_id = resp.json()['id']
    tag = Tag.objects.get(pk=tag_id)
    self.assertEqual(tag.value, "tag5")

  def test_tag_create_basic_auth(self):
    # Authenticate User
    authentication = HTTPBasicAuth(
      "admin@codio.com",
      "1234"
    )
    self.client.auth = authentication

    # Create Tag
    resp = self.client.post(self.url, {
      "value" : "tag5"
    })

    # Check Status
    self.assertEqual(resp.status_code, 201)
    # Check Tag
    tag_id = resp.json()['id']
    tag = Tag.objects.get(pk=tag_id)
    self.assertEqual(tag.value, "tag5")