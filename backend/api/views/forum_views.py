from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination

from core.models import Topic, Post
from ..serializers.core_serializers import (PostSerializer,
                                            TopicSerializer)



class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all().order_by('-created_at')
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['title']
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        topic_id = self.request.query_params.get('topic_id')
        if topic_id:
            return Post.objects.filter(topic_id=topic_id).order_by('created_at')
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)