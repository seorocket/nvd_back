from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter


from core.models import News, Announcement, Event, MapPoint
from ..serializers.core_serializers import (NewsSerializer, 
                                            AnnouncementSerializer, 
                                            EventSerializer, 
                                            MapPointSerializer)


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


