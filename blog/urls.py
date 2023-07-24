from django.urls import path
from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'


urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    # path('', views.PostListView.as_view(), name='post_list'),
    # class-based views have an as_view() class method which returns a function that
    # can be called when a request arrives for a URL matching the associated pattern.
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search')
]


# You can see all built-in template tags and filters at https://docs.djangoproject.com/en/3.0/ref/templates/builtins/.
# You can learn more about defining URL patterns with regular expressions at
# https://docs.djangoproject.com/en/3.0/ref/urls/#django.urls.re_path.
# If you haven't worked with regular expressions before, you might want to take a look at the
# Regular Expression HOWTO located at https://docs.python.org/3/howto/regex.html first.
