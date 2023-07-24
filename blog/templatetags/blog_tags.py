from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()
# Each module that contains template tags needs to define a variable called register to be a valid tag library.
# • simple_tag: Processes the data and returns a string
# • inclusion_tag: Processes the data and returns a rendered template


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}
# Using an inclusion tag, you can render a template with context variables returned by your template tag.
# After registering the template tag, you specify the template that will be rendered with the returned values using
# blog/post/latest_posts.html. Your template tag will accept an optional count parameter that defaults to 5.
# Inclusion tags have to return a dictionary of values, which is used as the context to render the specified template.


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
    # In addition to Count, Django offers the aggregation functions Avg, Max, Min, and Sum.
    # You can read more about aggregation functions at https://docs.djangoproject.com/en/3.0/topics/db/aggregation/.

# You will create a custom filter to enable you to use markdown syntax in your blog
# posts and then convert the post contents to HTML in the templates. Markdown
# is a plain-text formatting syntax that is very simple to use, and it's intended to be
# converted into HTML. You can write posts using simple markdown syntax and get
# the content automatically converted into HTML code.


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


# https://docs.djangoproject.com/en/3.0/howto/customtemplate-tags/.
# Django's built-in template filters at:
# https://docs.djangoproject.com/en/3.0/ref/templates/builtins/#built-in-filter-reference.
# You can find more information about custom filters at:
# https://docs.djangoproject.com/en/3.0/howto/custom-templatetags/#writing-custom-template-filters.
# You can learn the basics of the markdown format at:
# https://daringfireball.net/projects/markdown/basics.
