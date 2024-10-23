from rest_framework import generics, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers, vary_on_cookie
from blog.api.serializers import PostSerializer, UserSerializer, PostDetailSerializer, TagSerializer
from blog.models import Post, Tag
from blango_auth.models import User
from django.utils import timezone
from django.db.models import Q
from django.http import Http404
from blog.api.filters import PostFilterSet

# PostViewSet Subsutite below classes
# class PostList(generics.ListCreateAPIView):
#     authentication_classes = [SessionAuthentication]
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


# class PostDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostDetailSerializer


class PostViewSet(viewsets.ModelViewSet):
  queryset = Post.objects.all()
  # filterset_fields = ['author', 'tags']
  ordering_fields = ['published_at', 'author', 'tags', 'slug']
  filterset_class = PostFilterSet


  def get_queryset(self):
    queryset = self.queryset

    if self.request.user.is_anonymous:
      queryset = self.queryset.filter(published_at__lte=timezone.now())

    elif self.request.user.is_staff:
      queryset = self.queryset
    else :
      queryset = self.queryset.filter(
        Q(published_at__lte=timezone.now()) | Q(author=self.request.user)
      )

    # Filter URL
    time_period = self.kwargs.get("period_name")
    if not time_period:
      return queryset

    if time_period == "new":
      return queryset.filter(published_at__gte=(timezone.now() - timezone.timedelta(hours=1)))
    
    if time_period == "today":
      return queryset.filter(published_at__date=timezone.now().date())
    
    if time_period == "week":
      return queryset.filter(published_at__gte=(timezone.now() - timezone.timedelta(days=7)))

    raise Http404(
                f"Time period {time_period_name} is not valid, should be "
                f"'new', 'today' or 'week'"
            )

    

  def get_serializer_class(self):
    if self.action in ("list", "create"):
      return PostSerializer
    return PostDetailSerializer

  @method_decorator(cache_page(120))
  @method_decorator(vary_on_headers("Authorization", "Cookie"))
  def list(self, *args, **kwargs):
    return super(PostViewSet, self).list(*args, **kwargs)

  @method_decorator(cache_page(300))
  @method_decorator(vary_on_headers("Authorization", "Cookies"))
  @action(methods=['get'], detail=False, name="Posts by the logged in user")
  def mine(self, request):
    if request.user.is_anonymous:
      raise PermissionDenied("You must be logged in to see which Posts are yours")

    posts = self.get_queryset().filter(author=request.user)
    page = self.paginate_queryset(posts)

    if page:
      post_serializer = PostSerializer(
        page,
        many=True,
        context={
          "request" : request
        }
      )
      return self.get_paginated_response(post_serializer.data)
    else:
      posts_serializer = PostSerializer(
        posts,
        many=True,
        context={
          "request" : request
        }
      )

    return Response(posts_serializer.data)


class UserDetail(generics.RetrieveAPIView):
    lookup_field = "email"
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @method_decorator(cache_page(300))
    def get(self, *args, **kwargs):
      return super(UserDetail, self).get(*args, **kwargs)


class TagViewSet(viewsets.ModelViewSet):
  queryset = Tag.objects.all()
  serializer_class = TagSerializer


  
  @method_decorator(cache_page(300))
  def retieve(self, *args, **kwargs):
      return super(TagViewSet, self).retieve(*args, **kwargs)

  @method_decorator(cache_page(300))
  def list(self, *args, **kwargs):
      return super(TagViewSet, self).list(*args, **kwargs)

  @action(methods=['get'], detail=True, name="Posts with the Tag")
  def posts(self, request, pk=None):
    tag = self.get_object()
    page = self.paginate_queryset(tag.posts)
    if page:
      post_serializer = PostSerializer(
        page,
        context= {
          "request" : request
        },
        many=True
      )
      return self.get_paginated_response(post_serializer.data)
    else:
      post_serializer = PostSerializer(
        tag.posts,
        context= {
          "request" : request
        },
        many=True
      )

    return Response(post_serializer.data)