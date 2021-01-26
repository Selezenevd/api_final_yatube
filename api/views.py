import django_filters
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets, mixins, filters
from .models import Post, Comment, Follow, Group, User
from .permissions import IsOwnerOrReadOnly
from .serializers import (CommentSerializer, PostSerializer, FollowSerializer,
                          GroupSerializer)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,
                       filters.SearchFilter]
    filterset_fields = ['group']
    search_fields = ['group']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class GetPostViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,
                       filters.SearchFilter]


class FollowViewSet(GetPostViewSet):
    serializer_class = FollowSerializer
    filterset_fields = ['user']
    search_fields = ['user__username']

    def get_queryset(self):
        return self.request.user.following.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GroupViewSet(GetPostViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['title']
    search_fields = ['title']
