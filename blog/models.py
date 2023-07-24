from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    # This returns the current datetime in a timezone-aware format.
    created = models.DateTimeField(auto_now_add=True)
    # auto_now_add- the date will be saved automatically when creating an object.
    updated = models.DateTimeField(auto_now=True)
    # Since you are using auto_now here, the date will be updated automatically when saving an object.
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    # This field shows the status of a post. You use a choices parameter,
    # so the value of this field can only be set to one of the given choices.
    # You can find all field types at https://docs.djangoproject.com/en/3.0/ref/models/fields/.

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return f"Title: {self.title}, Author: {self.author}"

    objects = models.Manager()  # The default manager
    published = PublishedManager()  # Our custom manager

    def get_absolute_url(self):
        # You can learn more about the URLs utility functions at
        # https://docs.djangoproject.com/en/3.0/ref/urlresolvers/.
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day, self.slug])

    tags = TaggableManager()

# The sqlmigrate command takes the migration names and returns their SQL without executing it.
# Run the following command to inspect the SQL output of your first migration:
# python manage.py sqlmigrate blog 0001

# python manage.py makemigrations blog
# python manage.py migrate
# Django generates the table names by combining the application name and the lowercase name of the model (blog_post)

# There are two ways to add or customize managers for your models: you can
# add extra manager methods to an existing manager, or create a new manager by
# modifying the initial QuerySet that the manager returns. The first method provides
# you with a QuerySet API such as Post.objects.my_manager(), and the latter
# provides you with Post.my_manager.all(). The manager will allow you to
# retrieve posts using Post.published.all().
# The get_queryset() method of a manager returns the QuerySet that will be
# executed. You override this method to include your custom filter in the final
# QuerySet.


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
