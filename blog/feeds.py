from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Post
"""A web feed is a data format (usually XML) that provides users with the most recently updated content. 
Users will be able to subscribe to your feed using a feed aggregator 
(software that is used to read feeds and get new content notifications).
Read more about the Django syndication feed framework at https://docs.djangoproject.com/en/3.0/ref/contrib/syndication/."""


class LatestPostsFeed(Feed):
    title = 'My blog'
    link = reverse_lazy('blog:post_list')
    description = 'New posts of my blog.'
    # The reverse_lazy() utility function is a lazily evaluated version of reverse().

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 15)


# The item_title() and item_description() methods will receive each object returned by items() and
# return the title and description for each item.

