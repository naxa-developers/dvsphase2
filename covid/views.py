from rest_framework import viewsets, views
from rest_framework.response import Response

from .models import Ttmp
from .serializers import TtmpSerializer
from django_filters.rest_framework import DjangoFilterBackend


class TtmpViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'district_id', 'municipality_id', 'municipality_id']

    def get_queryset(self):
        queryset = Ttmp.objects.select_related('municipality_id', 'district_id', 'province_id',
                                               'program_id', 'supplier_id', 'partner_id').order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = TtmpSerializer
        return serializer_class
