from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter


from core.models import News, Announcement, Event, MapPoint, Topic, Post
from ..serializers.core_serializers import (NewsSerializer, 
                                            AnnouncementSerializer, 
                                            EventSerializer, 
                                            MapPointSerializer,
                                            PostSerializer,
                                            TopicSerializer)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.filter(is_active=True)
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [SearchFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'description']

class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class MapPointViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MapPoint.objects.all()
    serializer_class = MapPointSerializer

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all().order_by('-created_at')
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['title']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        topic_id = self.request.query_params.get('topic_id')
        if topic_id:
            return Post.objects.filter(topic_id=topic_id).order_by('created_at')
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)