from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from .views import *
from users.views import telegram_login, telegram_manual_register
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

router = DefaultRouter()

router.register(r'news', NewsViewSet)
router.register(r'announcements', AnnouncementViewSet)
router.register(r'events', EventViewSet)
router.register(r'map-points', MapPointViewSet)
router.register(r'gallery', GalleryViewSet)
router.register(r'organizations', OrgViewSet)
router.register(r'vacancy', VacancyViewSet)
router.register(r'attractions', AttrcationsViewSet)



urlpatterns = [
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('auth/telegram/login/', telegram_login, name='telegram-auth'),
    path('auth/telegram/register/', telegram_manual_register, name='telegram-manual-register'),
    path('', include(router.urls)),
    path('subscribe/', subscribe_to_newsletter, name='subscribe-newsletter'),
    path('feedback/', feedbackview, name='feedbackview'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]


