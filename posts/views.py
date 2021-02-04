from django.shortcuts import render, redirect
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from django.http import Http404
import random

from .models import Post
from .forms import PostForm

def feed(request):
    # This is the home page which renders posts from users
    # If logged in, it shows random posts from other users except yourself
    # Otherwise, it shows random posts from the database
    if request.user != AnonymousUser():
        # If logged in
        posts = list(Post.objects.exclude(owner=request.user))
    else:
        # If not logged in
        posts = list(Post.objects.all())
        
    random_posts = random.sample(posts, len(posts))
    context = {'posts': random_posts}
    return render(request, 'feed.html', context)

@login_required
def user_posts(request):
    # This view is for 'my posts' page which shows one user's own posts
    owner_posts = request.user.post_set.all().order_by('-date_added')
    context = {'owner_posts': owner_posts}
    return render(request, 'posts.html', context)

@login_required
def create_post(request):
    # This view is for creating new posts
    if request.method != 'POST':
        form = PostForm()
    else:
        form = PostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user
            new_post.save()
            return redirect('posts')

    context = {'form': form}
    return render(request, 'create_post.html', context)

@login_required
def edit_post(request, post_id):
    # This view is for editing existing posts of a user
    post = Post.objects.get(id=post_id)
    
    # If someone tries to edit other user's posts
    if request.user != post.owner:
        raise Http404

    if request.method != 'POST':
        form = PostForm(instance=post)
    else:
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts')

    context = {'form': form, 'post': post}
    return render(request, 'edit_post.html', context)

def search_results(request):
    # This view returns posts from the database that match
    # user's input words in the search bar which is case insensitive
    # It also shows number of matches and the matched words found
    # It outputs matched posts according to number of matched words

    # Get the query
    query = request.GET.get('q')
    # Split query into words
    query_list = query.split(' ')

    posts = list(Post.objects.all())
    posts_len = len(posts)
    posts_ids_counts = [[0, []] for i in range(posts_len)]

    # for every word find matched posts from the database
    for s in query_list:
        found = list(Post.objects.filter(text__icontains=s))
        for r in found:
            posts_ids_counts[r.id - 1][0] += 1
            posts_ids_counts[r.id - 1][1].append(s)

    make_context_object = []    # the object that will be returned to template
    make_context_set = []
    for i in range(posts_len):
        if posts_ids_counts[i][0]: # excluding 0 matches
            make_context_set.append((-posts_ids_counts[i][0], i + 1, posts_ids_counts[i][1]))
    make_context_set.sort()
    for i in make_context_set:
        yoo = Post.objects.get(id=i[1])
        yoo.count = -i[0]
        yoo.matches = i[2]
        make_context_object.append(yoo)

    context = {'posts': make_context_object}
    return render(request, 'search.html', context)
