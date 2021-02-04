from django.urls import path, include

from .views import feed, user_posts, create_post, edit_post, search_results

urlpatterns = [
    path('', feed, name='feed'),
    path('posts/', user_posts, name='posts'),
    path('create/', create_post, name='create_post'),
    path('edit_post/<int:post_id>/', edit_post, name='edit_post'),
    path('search/', search_results, name='search'),
]
