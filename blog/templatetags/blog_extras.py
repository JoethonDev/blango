from django.contrib.auth import get_user_model
from django import template
from django.utils.html import format_html
from blog.models import Post
import logging
# Low Level
# from django.utils.html import escape
# from django.utils.safestring import mark_safe

logger = logging.getLogger(__name__)
user_model = get_user_model()
register = template.Library()

# Filters
@register.filter
def author_details(author, current_user=None):
    if not isinstance(author, user_model):
        # return empty string as safe default
        return ""

    if author.username == current_user.username:
      return format_html("<strong>me</strong>")
    
    if author.first_name and author.last_name:
        name = f"{author.first_name} {author.last_name}"
    else:
        name = f"{author.username}"

    if author.email:
        # email = escape(author.email)
        # name = escape(name)
        return format_html('<a href="mailto:{}">{}</a>', author.email, name)

    return name

# Inclusion Tags
@register.inclusion_tag("blog/post-list.html")
def recent_posts(post):
  posts = Post.objects.exclude(pk=post.id).order_by("-published_at")[:5]
  logging.debug("Loaded %d recent posts for post %d", len(posts), post.pk)
  return {
    "posts" : posts,
    "title" : "Recent Posts"
  }



# Simple Tags
@register.simple_tag(takes_context=True)
def author_details_tag(context):
    request = context["request"]
    current_user = request.user
    post = context["post"]
    author = post.author

    if author.username == current_user.username:
      return format_html("<strong>me</strong>")
    
    if author.first_name and author.last_name:
        name = f"{author.first_name} {author.last_name}"
    else:
        name = f"{author.username}"

    if author.email:
        # email = escape(author.email)
        # name = escape(name)
        return format_html('<a href="mailto:{}">{}</a>', author.email, name)

    return name


@register.simple_tag
def row(extra_classes=""):
    return format_html('<div class="row {}">', extra_classes)


@register.simple_tag
def endrow():
    return format_html("</div>")


@register.simple_tag
def col(extra_classes=""):
    return format_html('<div class="col {}">', extra_classes)


@register.simple_tag
def endcol():
    return format_html("</div>")
# register.filter("author_details", author_details) 