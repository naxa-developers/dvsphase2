from .models import Partner, Program, MarkerValues, District, Province, GapaNapa, FiveW, Indicator, IndicatorValue, \
    Sector, SubSector, MarkerCategory, TravelTime, GisLayer, Project, Output, Notification, BudgetToSecondTier, \
    NepalSummary
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import PartnerSerializer, ProgramSerializer, MarkerValuesSerializer, DistrictSerializer, \
    ProvinceSerializer, GaanapaSerializer, FivewSerializer, \
    IndicatorSerializer, IndicatorValueSerializer, SectorSerializer, SubsectorSerializer, MarkerCategorySerializer, \
    TravelTimeSerializer, GisLayerSerializer, ProjectSerializer, OutputSerializer, NotificationSerializer, \
    ContractSumSerializer, NepalSummarySerializer
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
from django.db.models import Q


# Create your views here.
class ProgramSankey(viewsets.ModelViewSet):
    queryset = True
    serializer_class = FivewSerializer

    def list(self, request, *args, **kwargs):
        node = []
        links = []
        indexes = []
        program_id = []
        component_id = []
        partner_id = []
        if request.GET.getlist('program'):
            prov = request.GET['program']
            program_filter_id = prov.split(",")
            for i in range(0, len(program_filter_id)):
                program_filter_id[i] = int(program_filter_id[i])
        else:
            program_filter_id = list(Program.objects.values_list('id', flat=True))

        program = FiveW.objects.values('program_id__name', 'program_id', "program_id__code").exclude(
            allocated_budget=0).filter(
            program_id__in=program_filter_id).distinct('program_id')

        for p in program:
            print('program_name', p['program_id__name'])
            node.append({
                'name': p['program_id__name'],
                'type': 'program',
            })
            indexes.append(p['program_id__name'] + str(p['program_id__code']))
            program_id.append(p['program_id'])
        print('prog_list', indexes)
        component = FiveW.objects.values('component_id__name', 'component_id', 'component_id__code').exclude(
            allocated_budget=0).filter(
            program_id__in=program_filter_id).distinct(
            'component_id')
        for c in component:
            print(c['component_id__name'])
            node.append({
                'name': c['component_id__name'],
                'type': 'component',
            })
            indexes.append(c['component_id__name'] + str(c['component_id__code']))
            component_id.append(c['component_id'])
        print('com_list', indexes)
        partner = FiveW.objects.values('supplier_id__name', 'supplier_id', "supplier_id__code").exclude(
            allocated_budget=0).filter(
            program_id__in=program_filter_id).distinct('supplier_id')
        for part in partner:
            node.append({
                'name': part['supplier_id__name'],
                'type': 'partner',
            })
            indexes.append(part['supplier_id__name'] + str(part['supplier_id__code']))
            partner_id.append(part['supplier_id'])

        # allocated_sum = query.aggregate(Sum('allocated_budget'))
        # nodes = list(query) + list(comp) + list(part)
        for i in range(0, len(component_id)):
            q = FiveW.objects.values('id', 'component_id__name', 'component_id', 'component_id__code',
                                     'program_id__name',
                                     'program_id__code',
                                     'allocated_budget').exclude(allocated_budget=0).filter(
                component_id=component_id[i])
            print('id', q[0]['id'])
            print('com_1', q[0]['component_id__name'])
            print('prog_1', q[0]['program_id__name'])
            budget = q.aggregate(Sum('allocated_budget'))
            source = indexes.index(q[0]['program_id__name'] + str(q[0]['program_id__code']))
            target = indexes.index(q[0]['component_id__name'] + str(q[0]['component_id__code']))
            links.append({
                'source': source,
                'target': target,
                'value': budget['allocated_budget__sum'],
            })

        for i in range(0, len(component_id)):
            q = FiveW.objects.values('component_id__name', 'supplier_id', 'component_id__code',
                                     'supplier_id__name',
                                     'supplier_id__code',
                                     'allocated_budget').exclude(allocated_budget=0).filter(supplier_id__in=partner_id,
                                                                                            component_id=component_id[
                                                                                                i])

            budget = q.aggregate(Sum('allocated_budget'))
            source = indexes.index(q[0]['component_id__name'] + str(q[0]['component_id__code']))
            target = indexes.index(q[0]['supplier_id__name'] + str(q[0]['supplier_id__code']))
            links.append({
                'source': source,
                'target': target,
                'value': budget['allocated_budget__sum'],
            })

        return Response({"nodes": node, "links": links})


class RegionSankey(viewsets.ModelViewSet):
    queryset = True
    serializer_class = FivewSerializer

    def list(self, request, *args, **kwargs):
        node = []
        links = []
        indexes = []
        province_id = []
        district_id = []
        municipality_id = []

        # threshold = float(request.GET['threshold'])
        if request.GET.getlist('threshold'):
            threshold = float(request.GET['threshold'])

        else:
            threshold = 0.3

        if request.GET.getlist('province'):
            prov = request.GET['province']
            province_filter_id = prov.split(",")
            for i in range(0, len(province_filter_id)):
                province_filter_id[i] = int(province_filter_id[i])
        else:
            province_filter_id = list(Province.objects.exclude(code=-1).values_list('id', flat=True).distinct())
        if request.GET.getlist('program'):
            prov = request.GET['program']
            program_filter_id = prov.split(",")
            for i in range(0, len(program_filter_id)):
                program_filter_id[i] = int(program_filter_id[i])
        else:
            program_filter_id = list(Program.objects.values_list('id', flat=True))

        five_query = FiveW.objects.filter(province_id__in=province_filter_id, program_id__in=program_filter_id)

        total_budget_sum = five_query.aggregate(Sum('allocated_budget'))['allocated_budget__sum']

        percentage_one = int((total_budget_sum * threshold) / 100)
        province = five_query.values('province_id__name', 'province_id', "province_id__code").distinct(
            'province_id').exclude(allocated_budget__lt=percentage_one)
        for p in province:
            node.append({
                'name': p['province_id__name'],
                'type': 'province',
            })
            indexes.append(p['province_id__name'] + str(p['province_id__code']))
            province_id.append(p['province_id'])
        district = five_query.values('province_id', 'district_id__name', 'district_id',
                                     'district_id__code').distinct(
            'district_id').exclude(allocated_budget__lt=percentage_one).filter(~Q(district_id__code=-1))
        for c in district:
            node.append({
                'name': c['district_id__name'],
                'type': 'district',
            })
            indexes.append(c['district_id__name'] + str(c['district_id__code']))
            district_id.append(c['district_id'])
        municipality = five_query.values('province_id', 'municipality_id__name', 'municipality_id',
                                         "municipality_id__code").distinct('municipality_id').exclude(
            allocated_budget__lt=percentage_one).filter(~Q(municipality_id__code=-1))
        for part in municipality:
            node.append({
                'name': part['municipality_id__name'],
                'type': 'municipality',
            })
            indexes.append(part['municipality_id__name'] + str(part['municipality_id__code']))
            municipality_id.append(part['municipality_id'])
        for i in range(0, len(district_id)):
            q = five_query.values('district_id__name', 'district_id', 'district_id__code',
                                  'province_id__name',
                                  'province_id__code',
                                  'allocated_budget').filter(district_id=district_id[i]).exclude(
                allocated_budget__lt=percentage_one)

            budget = q.aggregate(Sum('allocated_budget'))
            source = indexes.index(q[0]['province_id__name'] + str(q[0]['province_id__code']))
            target = indexes.index(q[0]['district_id__name'] + str(q[0]['district_id__code']))
            links.append({
                'source': source,
                'target': target,
                'value': budget['allocated_budget__sum'],
            })

        for i in range(0, len(municipality_id)):
            q = five_query.values('province_id', 'district_id__name', 'municipality_id', 'district_id__code',
                                  'municipality_id__name',
                                  'municipality_id__code',
                                  'allocated_budget').filter(municipality_id=municipality_id[i]).exclude(
                allocated_budget__lt=percentage_one)

            budget = q.aggregate(Sum('allocated_budget'))
            source = indexes.index(q[0]['district_id__name'] + str(q[0]['district_id__code']))
            target = indexes.index(q[0]['municipality_id__name'] + str(q[0]['municipality_id__code']))
            links.append({
                'source': source,
                'target': target,
                'value': budget['allocated_budget__sum'],
            })

        return Response({"MaxThreshold": percentage_one, "nodes": node, "links": links})


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


class NepalSummaryApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']

    def get_queryset(self):
        queryset = NepalSummary.objects.order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = NepalSummarySerializer
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
            if cat_in.federal_level == 'district':
                indicator_dist = IndicatorValue.objects.values('id', 'indicator_id', 'value',
                                                               'district_id__code').filter(
                    indicator_id=id_indicator[i], )

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
        queryset = FiveW.objects.only('id', 'supplier_id', 'program_id', 'component_id', 'second_tier_partner',
                                      'province_id', 'district_id', 'municipality_id').order_by('id')

        return queryset

    def get_serializer_class(self):
        serializer_class = FivewSerializer
        return serializer_class

    # def get_serializer_context(self):
    #     context = super(Fivew, self).get_serializer_context()
    #     context.update({"request": self.request})
    #     return context


class FiveWDistrict(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = True
    serializer_class = FivewSerializer

    def list(self, request, *args, **kwargs):
        data = []
        programs = self.request.data
        program_d = programs['programId']
        if len(program_d) == 0:
            program = Program.objects.values_list('id', flat=True).order_by('id')
        else:
            program = programs['programId']
        districts = District.objects.values('name', 'id', 'code', 'n_code').exclude(code='-1').order_by('id')
        for dist in districts:
            query = FiveW.objects.values('allocated_budget', 'component_id', 'program_id').filter(
                district_id=dist['id'], program_id__in=program)
            if query:
                allocated_sum = query.aggregate(Sum('allocated_budget'))
                budget = allocated_sum['allocated_budget__sum']
                comp = query.values_list('component_id__name', flat=True).distinct()
                part = query.values_list('supplier_id__name', flat=True).distinct()
                sect = query.exclude(component_id__sector__name=None).values_list('component_id__sector__name',
                                                                                  flat=True).distinct()
                sub_sect = query.exclude(component_id__sub_sector__name=None).values_list(
                    'component_id__sub_sector__name',
                    flat=True).distinct()

            else:
                budget = 0
                comp = []
                part = []
                sect = []
                sub_sect = []

            data.append({
                'id': dist['id'],
                'name': dist['name'],
                'code': dist['code'],
                'allocated_budget': budget,
                'component': comp,
                'partner': part,
                'sector': sect,
                'sub_sector': sub_sect,

            })
        return Response({"results": data})


class FiveWProvince(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = True
    serializer_class = FivewSerializer

    def list(self, request, *args, **kwargs):
        data = []
        programs = self.request.data
        program_d = programs['programId']
        if len(program_d) == 0:
            program = Program.objects.values_list('id', flat=True).order_by('id')
        else:
            program = programs['programId']
        provinces = Province.objects.values('name', 'id', 'code').exclude(code='-1').order_by('id')
        for province in provinces:
            query = FiveW.objects.values('allocated_budget', 'component_id', 'program_id').filter(
                province_id=province['id'], program_id__in=program)
            if query:
                allocated_sum = query.aggregate(Sum('allocated_budget'))
                budget = allocated_sum['allocated_budget__sum']
                comp = query.values_list('component_id__name', flat=True).distinct()
                part = query.values_list('supplier_id__name', flat=True).distinct()
                sect = query.exclude(component_id__sector__name=None).values_list('component_id__sector__name',
                                                                                  flat=True).distinct()

                sub_sect = query.exclude(component_id__sub_sector__name=None).values_list(
                    'component_id__sub_sector__name',
                    flat=True).distinct()
                # mark_cat = query.exclude(component_id__sector__name=None).values_list(
                #     'program_id__marker_category__name', flat=True)

            else:
                budget = 0
                comp = []
                part = []
                sect = []
                sub_sect = []

            data.append({
                'id': province['id'],
                'name': province['name'],
                'code': str(province['code']),
                'allocated_budget': budget,
                'component': comp,
                'partner': part,
                'sector': sect,
                'sub_sector': sub_sect,

            })
        return Response({"results": data})


class FiveWMunicipality(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = True
    serializer_class = FivewSerializer

    def list(self, request, *args, **kwargs):
        data = []
        programs = self.request.data
        program_d = programs['programId']
        if len(program_d) == 0:
            program = Program.objects.values_list('id', flat=True).order_by('id')
        else:
            program = programs['programId']
        municipalities = GapaNapa.objects.values('name', 'id', 'code').exclude(code='-1').order_by('id')
        for municipality in municipalities:
            query = FiveW.objects.values('allocated_budget', 'component_id', 'program_id').filter(
                municipality_id=municipality['id'],
                program_id__in=program)
            if query:
                allocated_sum = query.aggregate(Sum('allocated_budget'))
                budget = allocated_sum['allocated_budget__sum']
                comp = query.values_list('component_id__name', flat=True).distinct()
                part = query.values_list('supplier_id__name', flat=True).distinct()
                sect = query.exclude(component_id__sector__name=None).values_list('component_id__sector__name',
                                                                                  flat=True).distinct()
                sub_sect = query.exclude(component_id__sub_sector__name=None).values_list(
                    'component_id__sub_sector__name', flat=True).distinct()

            else:
                budget = 0
                comp = []
                part = []
                sect = []
                sub_sect = []

            data.append({
                'id': municipality['id'],
                'name': municipality['name'],
                'code': str(municipality['code']),
                'allocated_budget': budget,
                'component': comp,
                'partner': part,
                'sector': sect,
                'sub_sector': sub_sect,

            })
        return Response({"results": data})


class SummaryData(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = True
    serializer_class = FivewSerializer

    def list(self, request, *args, **kwargs):
        programs = self.request.data
        program_d = programs['programId']
        if len(program_d) == 0:
            program = Program.objects.values_list('id', flat=True).order_by('id')
        else:
            program = programs['programId']
        query = FiveW.objects.filter(program_id__in=program)
        allocated_sum = query.aggregate(Sum('allocated_budget'))
        program = query.distinct('program_id').count()
        component = query.distinct('component_id').count()
        partner = query.distinct('supplier_id').count()
        sector = query.distinct('component_id__sector').count()

        return Response({
            'allocated_budget': allocated_sum['allocated_budget__sum'],
            'program': program,
            'partner': partner,
            'component': component,
            'sector': sector,

        })


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
    filterset_fields = ['id', 'category', 'indicator', 'is_covid', 'is_dashboard']

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
    filterset_fields = ['id', 'name', 'program_id', 'sector', 'sub_sector']

    def get_queryset(self):
        queryset = Project.objects.order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = ProjectSerializer
        return serializer_class


class ProgramTestApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name', 'marker_value', 'marker_category', ]

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
