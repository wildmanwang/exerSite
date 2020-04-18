from django.urls import re_path
from apps.blogs import views

urlpatterns = [
    re_path('blogNew', views.blogNew, name="blogNew"),
    re_path('index-(?P<pageNo>\d+)-(?P<category_id>\d+)-(?P<article_type_id>\d+)$', views.index, name="index"),
    re_path('blog-(?P<nid>\d+)', views.blog, name="blog"),
    re_path('blogZan$', views.blogZan, name="blogZan"),
]
