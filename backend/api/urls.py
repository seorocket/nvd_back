from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from .views import *
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

router = DefaultRouter()

router.register(r'news', NewsViewSet)
router.register(r'announcements', AnnouncementViewSet)
router.register(r'events', EventViewSet)
router.register(r'map-points', MapPointViewSet)


urlpatterns = [
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    path('subscribe/', subscribe_to_newsletter, name='subscribe-newsletter'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]


