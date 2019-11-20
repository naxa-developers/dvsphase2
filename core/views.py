from .models import Partner, Program, MarkerValues, District, Province, GapaNapa, FiveW, Indicator, IndicatorValue, \
    Sector, SubSector, MarkerCategory, TravelTime, GisLayer, Project, Output
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import PartnerSerializer, ProgramSerializer, MarkerValuesSerializer, DistrictSerializer, \
    ProvinceSerializer, GaanapaSerializer, FivewSerializer, \
    IndicatorSerializer, IndicatorValueSerializer, SectorSerializer, SubsectorSerializer, MarkerCategorySerializer, \
    TravelTimeSerializer, GisLayerSerializer, ProjectSerializer, OutputSerializer
from rest_framework import viewsets, views
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from django.db.models import Q
from django.db import connection
from django.http import Http404, HttpResponse


# Create your views here.


class PartnerView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']

    def get_queryset(self):
        queryset = Partner.objects.order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = PartnerSerializer
        return serializer_class


class MarkerCategoryApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']

    def get_queryset(self):
        queryset = MarkerCategory.objects.order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = MarkerCategorySerializer
        return serializer_class


class GisApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']

    def get_queryset(self):
        queryset = GisLayer.objects.order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = GisLayerSerializer
        return serializer_class


class MarkerValueApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'marker_category_id']

    def get_queryset(self):
        queryset = MarkerValues.objects.select_related('marker_category_id').order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = MarkerValuesSerializer
        return serializer_class


class DistrictApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'province_id']

    def get_queryset(self):
        queryset = District.objects.order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = DistrictSerializer
        return serializer_class


class ProvinceApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']

    def get_queryset(self):
        queryset = Province.objects.order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = ProvinceSerializer
        return serializer_class


class GapaNapaApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'province_id', 'district_id', 'hlcit_code', 'gn_type_en', 'gn_type_np']

    def get_queryset(self):
        queryset = GapaNapa.objects.select_related('province_id', 'district_id').order_by('id')
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


class IndicatorApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'category', 'indicator']

    def get_queryset(self):
        queryset = Indicator.objects.order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = IndicatorSerializer
        return serializer_class


class IndicatorData(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'indicator_id', 'gapanapa_id']

    def get_queryset(self):
        queryset = IndicatorValue.objects.select_related('gapanapa_id', 'indicator_id').order_by('id')
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


class OutputApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = []

    def get_queryset(self):
        queryset = Output.objects.order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = OutputSerializer
        return serializer_class


class SubsectorApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'sector_id', 'name']

    def get_queryset(self):
        queryset = SubSector.objects.select_related('sector_id').order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = SubsectorSerializer
        return serializer_class


class ProjectApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name']

    def get_queryset(self):
        queryset = Project.objects.order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = ProjectSerializer
        return serializer_class


class ProgramTestApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'marker_value', 'marker_category', 'sector', 'sub_sector']

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


def municipality_tile(request, zoom, x, y):
    """
    Custom view to serve Mapbox Vector Tiles for the custom polygon model.
    """

    if len(request.GET) == 0:
        sql_data = "SELECT ST_AsMVT(tile) FROM (SELECT id, name, hlcit_code, province_id_id, district_id_id, ST_AsMVTGeom(boundary, TileBBox(%s, %s, %s, 4326)) FROM  core_gapanapa) AS tile"
    else:
        try:
            mun = request.GET['palika']
            sql_data = "SELECT ST_AsMVT(tile) FROM (SELECT id, name, hlcit_code, province_id_id, district_id_id, ST_AsMVTGeom(boundary, TileBBox(%s, %s, %s, 4326)) FROM  core_gapanapa where id = " + mun + ") AS tile"
        except:
            print("")

        try:
            dist = request.GET['district']
            sql_data = "SELECT ST_AsMVT(tile) FROM (SELECT id, name, hlcit_code, province_id_id, district_id_id, ST_AsMVTGeom(boundary, TileBBox(%s, %s, %s, 4326)) FROM  core_gapanapa where district_id_id = " + dist + ") AS tile"
        except:
            print("")

        try:
            prov = request.GET['province']
            sql_data = "SELECT ST_AsMVT(tile) FROM (SELECT id, name, hlcit_code, province_id_id, district_id_id, ST_AsMVTGeom(boundary, TileBBox(%s, %s, %s, 4326)) FROM  core_gapanapa where province_id_id = " + prov + ") AS tile"
        except:
            print("")

    with connection.cursor() as cursor:
        cursor.execute(sql_data, [zoom, x, y])

        tile = bytes(cursor.fetchone()[0])
        # return HttpResponse(len(tile))

        if not len(tile):
            raise Http404()
    return HttpResponse(tile, content_type="application/x-protobuf")


def district_tile(request, zoom, x, y):
    """
    Custom view to serve Mapbox Vector Tiles for the custom polygon model.
    """

    if len(request.GET) == 0:
        sql_data = "SELECT ST_AsMVT(tile) FROM (SELECT id, name, code, province_id_id, ST_AsMVTGeom(boundary, TileBBox(%s, %s, %s, 4326)) FROM  core_district) AS tile"
    else:

        try:
            dist = request.GET['district']
            sql_data = "SELECT ST_AsMVT(tile) FROM (SELECT id, name, code, province_id_id, ST_AsMVTGeom(boundary, TileBBox(%s, %s, %s, 4326)) FROM  core_district where id = " + dist + ") AS tile"
        except:
            print("")

        try:
            prov = request.GET['province']
            sql_data = "SELECT ST_AsMVT(tile) FROM (SELECT id, name, code, province_id_id, ST_AsMVTGeom(boundary, TileBBox(%s, %s, %s, 4326)) FROM  core_district where province_id_id = " + prov + ") AS tile"
        except:
            print("")

    with connection.cursor() as cursor:
        cursor.execute(sql_data, [zoom, x, y])

        tile = bytes(cursor.fetchone()[0])
        # return HttpResponse(len(tile))

        if not len(tile):
            raise Http404()
    return HttpResponse(tile, content_type="application/x-protobuf")
