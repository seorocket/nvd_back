import django_filters
from core.models.core_models import News

class NewsFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(field_name='category__id')
    start_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = News
        fields = ['category', 'start_date', 'end_date']