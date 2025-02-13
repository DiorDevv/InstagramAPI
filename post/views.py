from unittest.async_case import IsolatedAsyncioTestCase

from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny

from .models import PostComment, PostLike, Post, CommentLike
from .serializers import PostSerializer, PostLikeSerializer, CommentLikeSerializer, CommentSerializer
from shared.cumtom_pagination import CustomPagination


class PostListView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Post.objects.all()


class PostCreateView(CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticated, ]
#
#     def get_queryset(self):
#         return Post.objects.all()
