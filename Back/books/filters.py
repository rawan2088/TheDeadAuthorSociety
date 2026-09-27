import django_filters
from books.models import Book

class BookListFilter(django_filters.FilterSet):
    is_available = django_filters.BooleanFilter(method='filter_is_available')
    # we don't need to set a method here because it is connected to a field and has a standard way to filter
    # a custom field would be when something isn't standard, like checking wether a field is there or not
    min_avg_rating = django_filters.NumberFilter(field_name='avg_rating', lookup_expr='gte')
    max_avg_rating = django_filters.NumberFilter(field_name='avg_rating', lookup_expr='lte')
    # the search query would be 
    # ?max_avg_rating=5&min_avg_rating=1
    
    published_year = django_filters.NumberFilter(field_name='published_date', lookup_expr='year')
    published_after = django_filters.NumberFilter(field_name='published_date', lookup_expr='year__gt')
    published_before = django_filters.NumberFilter(field_name='published_date', lookup_expr='year__lt')
    category_name = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')

    
    
    class Meta:
        model = Book
        
        # this is only exact filtering
        # fields = ['title', 'author', 'published_date', 'categories', 'is_available', 'avg_rating']
        
        fields = {
            # i is for insensitive
            'title': ['icontains'],
            'author': ['exact'],
            # http://127.0.0.1:8000/api/books/?published_date__year__gt=2020
            'published_date': ['exact'],
            # 'published_date': ['exact', 'year__exact', 'year__gt', 'year__lt'],
            'categories': ['exact'],
            # 'is_available': ['exact'], 
            # 'avg_rating': ['exact', 'lt', 'gt', 'range']
            #todo: fix these fields to allow filterization
        }    
        
    def filter_is_available(self, queryset, name, value):
        # relies on the view's queryset already being annotated
        # with available_copies (it already is, from BookListView)
        return queryset.filter(available_copies__gt=0) if value else queryset.filter(available_copies__lte=0)


