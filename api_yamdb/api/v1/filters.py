import django_filters

from reviews.models import Categories, Genres, Title


class TitleFilter(django_filters.FilterSet):
    """Фильтр  Title."""

    name = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.ModelChoiceFilter(
        field_name='category',
        queryset=Categories.objects.all(),
        to_field_name='slug'
    )
    genre = django_filters.ModelChoiceFilter(
        field_name='genre',
        queryset=Genres.objects.all(),
        to_field_name='slug'
    )

    class Meta:
        """Метаданные Title."""

        model = Title
        fields = ['category', 'genre', 'name', 'year']
