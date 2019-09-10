from .models import Partner, Program, MarkerValues, District, Province, GapaNapa, FiveW, Indicator, IndicatorValue, \
    Sector, SubSector, MarkerCategory
from rest_framework.permissions import AllowAny
from .serializers import PartnerSerializer, ProgramSerializer, MarkerValuesSerializer, DistrictSerializer, \
    ProvinceSerializer, GaanapaSerializer, FivewSerializer, \
    IndicatorSerializer, IndicatorValueSerializer, SectorSerializer, SubsectorSerializer, MarkerCategorySerializer
from rest_framework import viewsets, views
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
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


class ProgramView(views.APIView):
    """
    get: lists of program
            -example request url for search "/api/v1/core/program/?search=program_name/program_id"
    """
    permissions_classes = [AllowAny]

    def get(self, request):
        search_param = self.request.query_params.get('search', None)
        print(search_param)
        if search_param:
            queryset = Program.objects.filter(Q(program_name__icontains=search_param) | Q(id__icontains=search_param))
        else:
            queryset = Program.objects.all()

        print(queryset)
        serializer = ProgramSerializer(queryset, many=True)
        return Response({'heading': 'Heading of data', 'description': 'description of data', 'data': serializer.data})


class MarkerCategoryApi(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = MarkerCategory.objects.all()
        serializer = MarkerCategorySerializer(queryset, many=True)
        return Response({'heading': 'Heading of data', 'description': 'description of data', 'data': serializer.data})



class MarkerValueApi(views.APIView):
    permissions_classes = [AllowAny]

    def get(self, request):
        queryset = MarkerValues.objects.all()
        serializer = MarkerValuesSerializer(queryset, many=True)
        return Response({'heading': 'Heading of data', 'description': 'description of data', 'data': serializer.data})


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


class GapaNapaApi(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = GapaNapa.objects.select_related().all()
        serializer = GaanapaSerializer(queryset, many=True)
        return Response({'heading': 'Heading of data', 'description': 'description of data', 'data': serializer.data})


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


# class IndicatorValueApi(views.APIView):
#     permission_classes = [AllowAny]
#     pagination_class = LimitOffsetPagination
#
#     def get(self, request):
#         queryset = IndicatorValue.objects.all()
#         paginator = LimitOffsetPagination()
#         paginated_queryset = paginator.paginate_queryset(queryset, request)
#         serializer = IndicatorValueSerializer(queryset, many=True)
#         return Response({'heading': 'Heading of data', 'description': 'description of data', 'data': serializer.data})


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

    # print(queryset)
    # if(a=0){}
    # def list(self, request, *args, **kwargs):
    #     print(self.get_queryset())
    #     inidicator_data = self.serializer_class(self.get_queryset(), many=True).data
    #     return Response({'heading': 'Heading of data', 'description': 'description of data'})


class SectorApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = []

    def get_queryset(self):
        queryset = Sector.objects.all().order_by('id')
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
        queryset = Program.objects.all()
        return queryset

    def get_serializer_class(self):
        serializer_class = ProgramSerializer
        return serializer_class