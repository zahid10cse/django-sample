from django.db.models import Q

from core.models import Country


class CountryService:

    @staticmethod
    def get_search_query(filters=None):
        search_txt = filters.pop('name', None)
        if not search_txt:
            return None
        return Q(name__icontains=search_txt)

    @staticmethod
    def fetch(filters=None, user=None):
        try:
            queryset = Country.objects.all()
            search_txt = CountryService.get_search_query(filters)
            
            if search_txt:
                queryset = queryset.filter(search_txt)
        except Exception as e:
            return None, str(e)

        return queryset, None
