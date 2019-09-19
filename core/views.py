from .models import Partner, Program, MarkerValues, District, Province, GapaNapa, FiveW, Indicator, IndicatorValue, \
    Sector, SubSector, MarkerCategory, TravelTime
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import PartnerSerializer, ProgramSerializer, MarkerValuesSerializer, DistrictSerializer, \
    ProvinceSerializer, GaanapaSerializer, FivewSerializer, \
    IndicatorSerializer, IndicatorValueSerializer, SectorSerializer, SubsectorSerializer, MarkerCategorySerializer, \
    TravelTimeSerializer
from rest_framework import viewsets, views
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from django.db.models import Q


# Create your views here.


class PartnerView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        # print(request.user.group)
        # print(request.user.group)
        queryset = Partner.objects.all()
        serializer = PartnerSerializer(queryset, many=True)
        return Response({'heading': 'Heading of data', 'description': 'description of data', 'data': serializer.data})


class MarkerCategoryApi(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = MarkerCategory.objects.all()
        serializer = MarkerCategorySerializer(queryset, many=True)
        return Response({'heading': 'Heading of data', 'description': 'description of data', 'data': serializer.data})


class MarkerValueApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'marker_category']

    def get_queryset(self):
        queryset = MarkerValues.objects.select_related('marker_category').order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = MarkerValuesSerializer
        return serializer_class


class DistrictApi(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = District.objects.select_related().all()
        serializer = DistrictSerializer(queryset, many=True)
        return Response({'heading': 'Heading of data', 'description': 'description of data', 'data': serializer.data})


class ProvinceApi(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = Province.objects.all()
        serializer = ProvinceSerializer(queryset, many=True)
        return Response({'heading': 'Heading of data', 'description': 'description of data', 'data': serializer.data})


class GapaNapaApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'hlcit_code']

    def get_queryset(self):
        queryset = GapaNapa.objects.select_related('province', 'district').order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = GaanapaSerializer
        return serializer_class


class Fivew(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        queryset = FiveW.objects.select_related().all()
        serializer = FivewSerializer(queryset, many=True)
        return Response({'heading': 'Heading of dataa', 'description': 'description of data', 'data': serializer.data})


class IndicatorApi(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = Indicator.objects.all()
        serializer = IndicatorSerializer(queryset, many=True)
        return Response({'heading': 'Heading of data', 'description': 'description of data', 'data': serializer.data})


class IndicatorData(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'indicator', 'gapanapa']

    def get_queryset(self):
        queryset = IndicatorValue.objects.select_related('gapanapa', 'indicator').order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = IndicatorValueSerializer
        return serializer_class


class SectorApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = []

    def get_queryset(self):
        queryset = Sector.objects.order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = SectorSerializer
        return serializer_class


class SubsectorApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'sector', 'sub_sector_name']

    def get_queryset(self):
        queryset = SubSector.objects.select_related('sector').order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = SubsectorSerializer
        return serializer_class


class ProgramTestApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'marker', 'marker_category', 'sector', 'sub_sector']

    def get_queryset(self):
        queryset = Program.objects.order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = ProgramSerializer
        return serializer_class


class TravelTimeApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    # authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'gapanapa', 'facility_type', 'travel_category_population', 'season', 'travel_category']

    def get_queryset(self):
        queryset = TravelTime.objects.select_related('gapanapa').order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = TravelTimeSerializer
        return serializer_class
