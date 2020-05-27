from .models import Partner, Program, MarkerValues, District, Province, GapaNapa, FiveW, Indicator, IndicatorValue, \
    Sector, SubSector, MarkerCategory, TravelTime, GisLayer, Project, Output, Notification, BudgetToSecondTier
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import PartnerSerializer, ProgramSerializer, MarkerValuesSerializer, DistrictSerializer, \
    ProvinceSerializer, GaanapaSerializer, FivewSerializer, \
    IndicatorSerializer, IndicatorValueSerializer, SectorSerializer, SubsectorSerializer, MarkerCategorySerializer, \
    TravelTimeSerializer, GisLayerSerializer, ProjectSerializer, OutputSerializer, NotificationSerializer, \
    ContractSumSerializer
from rest_framework import viewsets, views
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from django.db.models import Q
from django.db import connection
from django.http import Http404, HttpResponse
import json
from django.db.models import Sum
import math


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


class DistrictIndicator(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = True
    serializer_class = DistrictSerializer

    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['id']

    def list(self, request, **kwargs):
        """
            *required= id of indicator as param{indicator_id} send as get request - /district-indicator/?indicator_id={indicator_id}
            """
        data = []
        district = District.objects.values('name', 'id', 'n_code', 'code').exclude(code=-1).order_by('id')
        id_indicators = request.data
        id_indicator = id_indicators['indicatorId']
        health_id = Indicator.objects.get(indicator='number_hospitals')
        health_id_b = Indicator.objects.get(indicator='household_affected_covid')
        for i in range(0, len(id_indicator)):
            cat_in = Indicator.objects.get(id=int(id_indicator[i]))
            if cat_in.federal_level == 'district level':
                indicator_dist = IndicatorValue.objects.values('id', 'indicator_id', 'value',
                                                               'district_id__code').filter(
                    indicator_id=id_indicator, )

                for dist_ind in indicator_dist:
                    data.append(
                        {
                            'id': dist_ind['id'],
                            'indicator_id': int(id_indicator[i]),
                            'code': dist_ind['district_id__code'],
                            'value': dist_ind['value']

                        }
                    )
                print('market')
            else:
                # print(health_id.id)
                for dist in district:
                    indicator = IndicatorValue.objects.values('id', 'indicator_id', 'value',
                                                              'gapanapa_id__population').filter(
                        indicator_id=int(id_indicator[i]),
                        gapanapa_id__district_id=dist['id'])
                    if int(id_indicator[i]) != health_id.id and int(id_indicator[i]) != health_id_b.id:
                        value_sum = 0
                        dist_pop_sum = GapaNapa.objects.values('name', 'id', 'district_id', 'population').filter(
                            district_id=dist['id']).aggregate(
                            Sum('population'))

                        for ind in indicator:
                            # print(ind['value'])
                            # print(math.isnan(ind['value']))

                            if math.isnan(ind['value']) == False:
                                indicator_value = (ind['value'] * ind['gapanapa_id__population'])
                                # print(indicator_value)
                                value_sum = (value_sum + indicator_value)
                            else:
                                value_sum = (value_sum + 0)

                        # print(value_sum)
                        # print(dist_pop_sum['population__sum'])
                        value = (value_sum / dist_pop_sum['population__sum'])
                    else:
                        dist_health_num = IndicatorValue.objects.values('id', 'value', 'gapanapa_id').filter(
                            indicator_id=int(id_indicator[i]),
                            gapanapa_id__district_id=dist['id']).aggregate(
                            Sum('value'))
                        value = dist_health_num['value__sum']

                    data.append(
                        {
                            'id': dist['id'],
                            'indicator_id': int(id_indicator[i]),
                            'code': dist['code'],
                            'value': value

                        }
                    )

        return Response({"results": data})


class ProvinceIndicator(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = True
    serializer_class = ProvinceSerializer

    def list(self, request, **kwargs):
        """
        *required= id of indicator as param{indicator_id} send as get request - /province-indicator/?indicator_id={indicator_id}
        """
        data = []
        total = []
        province = Province.objects.values('name', 'id', 'code').exclude(code=-1).order_by('id')
        id_indicators = request.data
        id_indicator = id_indicators['indicatorId']
        health_id = Indicator.objects.get(indicator='number_hospitals')
        health_id_b = Indicator.objects.get(indicator='household_affected_covid')
        for i in range(0, len(id_indicator)):
            for dist in province:
                if int(id_indicator[i]) != health_id.id and int(id_indicator[i]) != health_id_b.id:
                    value_sum = 0
                    dist_pop_sum = GapaNapa.objects.values('name', 'id', 'district_id', 'population').filter(
                        province_id=dist['id']).aggregate(
                        Sum('population'))
                    indicator = IndicatorValue.objects.values('id', 'indicator_id', 'value',
                                                              'gapanapa_id__population').filter(
                        indicator_id=int(id_indicator[i]),
                        gapanapa_id__province_id=dist['id'])
                    for ind in indicator:
                        # print(ind['value'])
                        # print(dist_pop_sum['population__sum'])
                        # print(math.isnan(ind['value']))

                        if math.isnan(ind['value']) == False:
                            indicator_value = (ind['value'] * ind['gapanapa_id__population'])
                            # print(indicator_value)
                            value_sum = (value_sum + indicator_value)
                        else:
                            value_sum = (value_sum + 0)

                    # print(value_sum)
                    # print(dist_pop_sum)
                    value = (value_sum / dist_pop_sum['population__sum'])

                else:
                    prov_health_num = IndicatorValue.objects.values('id', 'indicator_id', 'value',
                                                                    'gapanapa_id__population').filter(
                        indicator_id=int(id_indicator[i]),
                        gapanapa_id__province_id=dist['id']).aggregate(
                        Sum('value'))

                    value = prov_health_num['value__sum']

                data.append(
                    {
                        'id': dist['id'],
                        'indicator_id': int(id_indicator[i]),
                        'code': dist['code'],
                        # 'value_sum': value_sum,
                        # 'population': dist_pop_sum['population__sum'],
                        'value': value

                    }
                )

        return Response({"results": data})


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
        queryset = District.objects.exclude(code=-1).order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = DistrictSerializer
        return serializer_class


class ProvinceApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']

    def get_queryset(self):
        queryset = Province.objects.exclude(code=-1).order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = ProvinceSerializer
        return serializer_class


class GapaNapaApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'province_id', 'district_id', 'hlcit_code', 'gn_type_en', 'gn_type_np']
    queryset = GapaNapa.objects.only('id', 'province_id', 'district_id', 'hlcit_code', 'name', 'gn_type_np',
                                     'code', 'population').exclude(code=-1).order_by('id')
    serializer_class = GaanapaSerializer


class Fivew(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'supplier_id', 'program_id', 'component_id', 'second_tier_partner', 'province_id',
                        'district_id', 'municipality_id']

    def get_queryset(self):
        queryset = FiveW.objects.order_by('id')

        return queryset

    def get_serializer_class(self):
        serializer_class = FivewSerializer
        return serializer_class

    def get_serializer_context(self):
        context = super(Fivew, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class FiveWDistrict(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = True
    serializer_class = FivewSerializer

    def list(self, request, *args, **kwargs):
        data = []
        districts = District.objects.values('name', 'id', 'code', 'n_code').order_by('id')
        for dist in districts:
            allocated_sum = FiveW.objects.filter(district_id=dist['id']).aggregate(Sum('allocated_budget'))
            male_beneficiary_sum = FiveW.objects.filter(district_id=dist['id']).aggregate(Sum('male_beneficiary'))
            female_beneficiary_sum = FiveW.objects.filter(district_id=dist['id']).aggregate(Sum('female_beneficiary'))
            total_beneficiary_sum = FiveW.objects.filter(district_id=dist['id']).aggregate(Sum('total_beneficiary'))

            data.append({
                'id': dist['id'],
                'name': dist['name'],
                'code': dist['code'],
                'allocated_budget': allocated_sum['allocated_budget__sum'],
                'male_beneficiary': male_beneficiary_sum['male_beneficiary__sum'],
                'female_beneficiary': female_beneficiary_sum['female_beneficiary__sum'],
                'total_beneficiary': total_beneficiary_sum['total_beneficiary__sum'],
            })
        return Response({"results": data})


class FiveWProvince(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = True
    serializer_class = FivewSerializer

    def list(self, request, *args, **kwargs):
        data = []
        provinces = Province.objects.values('name', 'id', 'code').order_by('id')
        for province in provinces:
            allocated_sum = FiveW.objects.filter(province_id=province['id']).aggregate(Sum('allocated_budget'))
            male_beneficiary_sum = FiveW.objects.filter(province_id=province['id']).aggregate(Sum('male_beneficiary'))
            female_beneficiary_sum = FiveW.objects.filter(province_id=province['id']).aggregate(
                Sum('female_beneficiary'))
            total_beneficiary_sum = FiveW.objects.filter(province_id=province['id']).aggregate(Sum('total_beneficiary'))

            data.append({
                'id': province['id'],
                'name': province['name'],
                'code': str(province['code']),
                'allocated_budget': allocated_sum['allocated_budget__sum'],
                'male_beneficiary': male_beneficiary_sum['male_beneficiary__sum'],
                'female_beneficiary': female_beneficiary_sum['female_beneficiary__sum'],
                'total_beneficiary': total_beneficiary_sum['total_beneficiary__sum'],
            })
        return Response({"results": data})


class FiveWMunicipality(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = True
    serializer_class = FivewSerializer

    def list(self, request, *args, **kwargs):
        data = []
        municipalities = GapaNapa.objects.values('name', 'id', 'code').order_by('id')
        for municipality in municipalities:
            allocated_sum = FiveW.objects.filter(municipality_id=municipality['id']).aggregate(Sum('allocated_budget'))
            male_beneficiary_sum = FiveW.objects.filter(municipality_id=municipality['id']).aggregate(
                Sum('male_beneficiary'))
            female_beneficiary_sum = FiveW.objects.filter(municipality_id=municipality['id']).aggregate(
                Sum('female_beneficiary'))
            total_beneficiary_sum = FiveW.objects.filter(municipality_id=municipality['id']).aggregate(
                Sum('total_beneficiary'))

            data.append({
                'id': municipality['id'],
                'name': municipality['name'],
                'code': str(municipality['code']),
                'allocated_budget': allocated_sum['allocated_budget__sum'],
                'male_beneficiary': male_beneficiary_sum['male_beneficiary__sum'],
                'female_beneficiary': female_beneficiary_sum['female_beneficiary__sum'],
                'total_beneficiary': total_beneficiary_sum['total_beneficiary__sum'],
            })
        return Response({"results": data})


class ContractSum(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]

    # filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'supplier_id', 'program_id', 'component_id', 'second_tier_partner', ]

    def get_queryset(self):
        queryset = BudgetToSecondTier.objects.order_by('id')

        return queryset

    def get_serializer_class(self):
        serializer_class = ContractSumSerializer
        return serializer_class


class IndicatorApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'category', 'indicator', 'is_covid']

    def get_queryset(self):
        queryset = Indicator.objects.exclude(show_flag=False).order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = IndicatorSerializer
        return serializer_class


class IndicatorData(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'indicator_id', 'gapanapa_id']

    def get_queryset(self):
        id_indicators = self.request.data
        id_indicator = id_indicators['indicatorId']

        for i in range(0, len(id_indicator)):
            id_indicator[i] = int(id_indicator[i])
        queryset = IndicatorValue.objects.filter(indicator_id__in=id_indicator).select_related('gapanapa_id',
                                                                                               'indicator_id').order_by(
            'id')

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


class NotifyApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]

    # authentication_classes = (TokenAuthentication, BasicAuthentication)

    def get_queryset(self):
        queryset = Notification.objects.order_by('-id')
        return queryset

    def get_serializer_class(self):
        serializer_class = NotificationSerializer
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
    filterset_fields = ['id', 'name', 'program_id']

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
    # authentication_classes = (TokenAuthentication, BasicAuthentication)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'gapanapa', 'facility_type', 'travel_category_population', 'season', 'travel_category']

    def get_queryset(self):
        queryset = TravelTime.objects.select_related('gapanapa').order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = TravelTimeSerializer
        return serializer_class
