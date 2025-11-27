import django_filters
from core.models.core_models import News, Announcement, Event
from django.db import models


class NewsFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(field_name='category__id')
    start_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = News
        fields = ['category', 'start_date', 'end_date', 'search']

    def filter_search(self, queryset, name, value):
        if value:
            return queryset.filter(
                models.Q(title__icontains=value) |
                models.Q(content__icontains=value)
            )
        return queryset

class EventFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    date_start = django_filters.DateTimeFilter(field_name='date_time', lookup_expr='gte')
    date_end = django_filters.DateTimeFilter(field_name='date_time', lookup_expr='lte')
    category_id = django_filters.NumberFilter(field_name='category__id')
    class Meta:
        model = Event
        fields = ['search', 'date_start', 'date_end', 'category_id']

    def filter_search(self, queryset, name, value):
        """
        Кастомный метод для поиска по заголовку и описанию.
        """
        if value:
            return queryset.filter(
                models.Q(title__icontains=value) |
                models.Q(description__icontains=value)
            )
        return queryset


class AnnouncementFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    category_id = django_filters.ChoiceFilter(
        field_name='category', 
        choices=Announcement.CATEGORY_CHOICES, 
        label='Категория'
    )
    published_date_start = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    published_date_end = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Announcement
        fields = [ 'search', 'category_id', 'published_date_start', 'published_date_end']

    def filter_search(self, queryset, name, value):
        """
        Кастомный метод для поиска по заголовку и описанию.
        """
        if value:
            return queryset.filter(
                models.Q(title__icontains=value) |
                models.Q(description__icontains=value)
            )
        return queryset
    
