from django.urls import path
from .views import (PostListView, PostCreateView, PostRetrieveUpdateDestroyView, CommentListView,
                    PostCommentCreateView, CommentCreateView, CommentListCreateAPIView)

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/create/', PostCreateView.as_view(), name='post-create'),
    path('posts/<uuid:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post-create-update'),
    path('posts/<uuid:id>/comments/', CommentListView.as_view(), name='comment-list'),
    path('posts/<uuid:id>/comments/create/', PostCommentCreateView.as_view(), name='comment-create'),
    path('posts/comment/create/', CommentCreateView.as_view(), name='comment-create'),
    path('posts/comment/', CommentListCreateAPIView.as_view(), name='post-create'),
]
