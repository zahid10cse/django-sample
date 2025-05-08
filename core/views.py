from rest_framework import mixins
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from core.models import Country
from core.serializers import CountrySerializer
from core.services.country_service import CountryService
from mixins.response import api_response


class CoreViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        filters = request.query_params.dict()

        # Remove pagination parameters
        filters.pop('page', None)
        filters.pop('page_size', None)
        paginate = filters.pop('paginate', 'true').lower()

        countries, error = CountryService.fetch(filters)
        if error:
            raise ValidationError(error)

        if paginate != 'false':
            page = self.paginate_queryset(countries)
            if page is not None:
                serializer = self.get_paginated_response(CountrySerializer(page, many=True).data)
                return api_response(data=serializer.data.get('results', []), pagination=serializer.data)
        serializer = CountrySerializer(countries, many=True)
        return api_response(data=serializer.data)
