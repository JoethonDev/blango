from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.views.decorators.vary import vary_on_cookie
from blog.models import Post
from blog.forms import CommentForm
import logging

# Add Logger
logger = logging.getLogger(__name__)

# Create your views here.
# @cache_page(timeout=300)
# @vary_on_headers("Cookie") Alternative
# @vary_on_cookie
def index(request):
    posts = Post.objects.filter(published_at__lte=timezone.now())
    logger.debug(f"Posts Retrieved : {len(posts)}")
    return render(request, "blog/index.html", {"posts": posts})

def post_detail(request, slug):
    # Get Post
    post = get_object_or_404(Post, slug=slug)
    
    # Check if user is logged
    if request.user.is_active:
      # Request is POST
      if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
          comment = comment_form.save(commit=False)
          comment.content_object = post
          comment.creator = request.user
          comment.save()
          logger.info(
              "Created comment on Post %d for user %s", post.pk, request.user
          )
          # return redirect(reverse("blog-post-detail"))
          return redirect(request.path_info)
      else:
        comment_form = CommentForm()

    else:
        comment_form = None

    return render(request, "blog/post-detail.html", {
      "post": post,
      "comment_form": comment_form
    })