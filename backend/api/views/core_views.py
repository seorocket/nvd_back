from rest_framework import viewsets, permissions, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from ..filters import AnnouncementFilter, EventFilter

from core.models import News, Announcement, Event, MapPoint, Gallery, Organization, Vacancy, Attractions
from ..serializers.core_serializers import (NewsSerializer, 
                                            AnnouncementSerializer, 
                                            EventSerializer, 
                                            MapPointSerializer,
                                            GallerySerializer,
                                            FeedBackSerializer,
                                            OrgSerializer,
                                            VacancySerializer,
                                            AttractionsSerializer)



class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    pagination_class = LimitOffsetPagination


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.filter(is_active=True)
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = AnnouncementFilter
    pagination_class = LimitOffsetPagination
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = EventFilter
    pagination_class = LimitOffsetPagination
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']


class MapPointViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MapPoint.objects.all()
    serializer_class = MapPointSerializer


class GalleryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GallerySerializer
    queryset = Gallery.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination

class OrgViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrgSerializer
    queryset = Organization.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination

class VacancyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VacancySerializer
    queryset = Vacancy.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination

class AttrcationsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AttractionsSerializer
    queryset = Attractions.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination


@api_view(['POST'])
def feedbackview(request):
    serializer = FeedBackSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response({
                "message": "Фидбек отправлен",
                "email": serializer.data['email']
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                "error": "Произошла ошибка при отправке.",
                "details": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)