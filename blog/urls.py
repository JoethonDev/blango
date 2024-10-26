# other imports
from django.urls import path
import blog.views

urlpatterns = [
    # other patterns
    path("", blog.views.index),
    path("post/<slug>/", blog.views.post_detail, name="blog-post-detail"),
    path("ip/", blog.views.get_ip),
    path("post-table/", blog.views.post_table, name="blog-post-table"),
]