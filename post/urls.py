from django.urls import path
from .views import PostListView, PostCreateView, PostRetrieveUpdateDestroyView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/create/', PostCreateView.as_view(), name='post-create'),
    path('posts/<uuid:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post-create-update'),
]
