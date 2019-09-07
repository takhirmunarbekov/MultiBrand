import django_filters as filters

from .models import (
    Category,
    Item,
)


# def categories(request):
#     if request is None:
#         return Category.objects.none()
#     return Category.objects.all()

class ItemFilter(filters.FilterSet):

    # category = filters.ModelChoiceFilter(queryset=categories)

    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')

    # name = filters.CharFilter(lookup_expr='icontains')

    # vendor_code = None
    # amount = None
    # price = None
    # is_new = None
    # is_hit = None
    # is_popular = None

    class Meta:
        model = Item
        fields = [
            'name',
            'category',
            'is_new',
            'is_hit',
            'is_popular',
        ]