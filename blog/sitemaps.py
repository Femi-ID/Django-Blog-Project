"""sitemap is an XML file that tells search engines the pages of your website, their relevance,
and how frequently they are updated. Using a sitemap will make your site more visible in
search engine rankings: sitemaps help crawlers to index your website's content."""

from django.contrib.sitemaps import Sitemap
from .models import Post
# complete sitemap reference in the official Django documentation located at
# https://docs.djangoproject.com/en/3.0/ref/contrib/sitemaps/.


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    # The changefreq and priority attributes indicate the change frequency
    # of your post pages and their relevance in your website (the maximum value is 1).

    def items(self):
        return Post.published.all()
    # The items() method returns the QuerySet of objects to include in this sitemap. By
    # default, Django calls the get_absolute_url() method on each object to retrieve its URL.

    def lastmod(self, obj):
        return obj.updated
    # The lastmod method receives each object returned by items() and returns the last
    # time the object was modified.

