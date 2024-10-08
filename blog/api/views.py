from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, AuthorModifyOrReadOnly, IsAdminUserForObject
# from rest_framework.permissions import 
from blog.api.serializers import PostSerializer, UserSerializer, PostDetailSerializer
from blog.models import Post
from blango_auth.models import User


class PostList(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer


class UserDetail(generics.RetrieveAPIView):
    lookup_field = "email"
    queryset = User.objects.all()
    serializer_class = UserSerializer