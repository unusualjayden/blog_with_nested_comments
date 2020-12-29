from django.urls import path

from .views import (
    PostListAPIView,
    PostDetailAPIView,
    CommentListAPIView,
    CommentDetailAPIView,
    CommentRepliesAPIView
)

app_name = 'posts-api'

urlpatterns = [
    path('posts/', PostListAPIView.as_view(), name='list'),
    path('posts/<int:post_id>/', PostDetailAPIView.as_view(), name='detail'),
    path('posts/<int:post_id>/comments/', CommentListAPIView.as_view(), name='comment-list'),
    path('posts/<int:post_id>/comments/<int:comment_id>/', CommentDetailAPIView.as_view(), name='comment-detail'),
    path('posts/<int:post_id>/comments/<int:comment_id>/replies/', CommentRepliesAPIView.as_view(), name='comment-replies')
]
