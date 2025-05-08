from django.db.models import Q

from core.models import Country


class CountryService:

    @staticmethod
    def get_search_query(filters=None):
        search_txt = filters.pop('search', None)
        if not search_txt:
            return None
        return Q(name__icontains=search_txt)

    @staticmethod
    def get_filter_objects(filters=None, user=None):
        """
        Generate filters for querying Stock objects with required field validation.
        :param filters: Dictionary of filter parameters
        :return: Filter dictionary
        :raises ValueError: If any required field is missing
        """

        if not filters:
            return {}

        # Create filter mapping for the fields and corresponding lookup expressions
        field_lookup_map = {
            'type': 'type',
        }

        # # Use dictionary comprehension to build the filter dictionary
        f_filter = {
            lookup: filters[field]
            for field, lookup in field_lookup_map.items()
            if filters.get(field) is not None  # Exclude fields with None values
        }
        return f_filter

    @staticmethod
    def fetch(filters=None, user=None):

        queryset = Country.objects.all().order_by('-id')

        f_filters = CountryService.get_filter_objects(filters, user)
        search_txt = CountryService.get_search_query(filters)
        try:
            queryset = queryset.filter(**f_filters)
            if search_txt:
                queryset = queryset.filter(search_txt)
        except Exception as e:
            return None, str(e)

        return queryset, None
