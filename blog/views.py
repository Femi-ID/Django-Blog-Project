from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
# You can learn about aggregation at https://docs.djangoproject.com/en/3.0/topics/db/aggregation/.
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery, TrigramWordSimilarity

# Create your views here.
# A Django view is just a Python function that receives a web request and returns a web response.


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # ... send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n {cd['name']}'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
            # The send_mail() function takes the subject, message, sender, and list of recipients as required arguments
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_list(request, tag_slug=None):
    object_list = Post.published.all()  # query for all posts where: status=published.
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)  # to display 3 posts in each page
    page = request.GET.get('page')  # to get the current page number
    try:
        posts = paginator.page(page)
        # You obtain the objects for the desired page by calling the page() method of Paginator.
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver the last page
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts': posts, 'page': page, 'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year, publish__month=month,
                             publish__day=day)

    # List of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet. The save() method is available for ModelForm
            # but not for Form instances, since they are not linked to any model.
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # post.comments.add(new_comment)
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'new_comment': new_comment,
                                                     'comment_form': comment_form, 'similar_posts': similar_posts})


def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            results = Post.published.annotate(rank=SearchRank(search_vector, search_query))\
                .filter(rank__gte=0.3).order_by('-rank')
            # The default weights are D, C, B, and A, and they refer to
            # the numbers 0.1, 0.2, 0.4, and 1.0, respectively.
            # A trigram is a group of three consecutive characters.
            # You can measure the similarity of two strings by counting the number of trigrams that they share.
            # results = Post.published.annotate(similarity=TrigramWordSimilarity('title', query))\
            #     .filter(similarity__gte=0.3).order_by('-similarity')
            # You can find more information about full-text search at
            # https://docs.djangoproject.com/en/3.0/ref/contrib/postgres/search/.
    return render(request, 'blog/post/search.html', {'form': form, 'query': query, 'results': results})

# Stemming is the process of reducing words to their word stem, base, or root form.
# Stemming is used by search engines to reduce indexed words to their stem, and to
# be able to match inflected or derived words.
# PostgreSQL provides a ranking function that orders results based on how often the
# query terms appear and how close together they are.
#

