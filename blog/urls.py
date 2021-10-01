from django.urls import path
from .views import (
    PostListView,
    OrderedPostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    MyPostListView,
    ThreadPostListView,
    TypePostListView,
    ThreadTypePostListView,
    like_view,
    dislike_view,
    list_esami_view,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    LikedPostListView
)

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),  # è una class-based view, quindi serve as_view()
    path('home/<str:order>', OrderedPostListView.as_view(), name='blog-home-order'),
    path('home/<str:username>/<str:order>', MyPostListView.as_view(), name='blog-myhome'),
    path('home/thread/<str:thread>/<str:order>', ThreadPostListView.as_view(), name='blog-thread'),
    path('home/type/<str:type>/<str:order>', TypePostListView.as_view(), name='blog-type'),
    path('home/thread/<str:thread>/type/<str:type>/<str:order>', ThreadTypePostListView.as_view(),
         name='blog-thread-type'),
    path('user/<str:username>/<str:order>', UserPostListView.as_view(), name='user-posts'),
    path('liked/<str:order>', LikedPostListView.as_view(), name='liked-posts'),

    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),  # la PrimaryKey di un post è un int
    path('post/new', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),

    path('comment/new/<int:pk>', CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/<int:pkp>/delete', CommentDeleteView.as_view(), name='comment-delete'),

    path('like/<int:post_id>', like_view, name='like_post'),
    path('dislike/<int:post_id>', dislike_view, name='dislike_post'),
    path('list/<str:periodo>', list_esami_view, name='list_esami_view')
]
