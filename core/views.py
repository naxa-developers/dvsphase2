from .models import Partner, Program, MarkerValues, District, Province, GapaNapa, FiveW, Indicator, IndicatorValue, \
    Sector, SubSector, MarkerCategory, TravelTime, GisLayer, Project, Output, Notification, BudgetToSecondTier, \
    NepalSummary, FeedbackForm, FAQ, TermsAndCondition, NationalStatistic, Manual
from dashboard.models import UserProfile
from django.contrib.auth.models import User, Group, Permission
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import PartnerSerializer, ProgramSerializer, MarkerValuesSerializer, DistrictSerializer, \
    ProvinceSerializer, GaanapaSerializer, FivewSerializer, \
    IndicatorSerializer, IndicatorValueSerializer, SectorSerializer, SubsectorSerializer, MarkerCategorySerializer, \
    TravelTimeSerializer, GisLayerSerializer, ProjectSerializer, OutputSerializer, NotificationSerializer, \
    ContractSumSerializer, NepalSummarySerializer, FeedbackSerializer, TermsAndConditionSerializer, FAQSerializer, \
    NetionalStatisticSerializer, ManualSerializer
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
from rest_framework.parsers import MultiPartParser, FormParser
from .filters import fivew, fivew_province, fivew_district, fivew_municipality, sankey
from datetime import datetime, date
from django.db.models import Q
from datetimerange import DateTimeRange


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
        if request.GET.getlist('threshold'):
            threshold = float(request.GET['threshold'])

        else:
            threshold = 0.0001

        if request.GET.getlist('program'):
            prov = request.GET['program']
            program_filter_id = prov.split(",")
            for i in range(0, len(program_filter_id)):
                program_filter_id[i] = int(program_filter_id[i])
        else:
            program_filter_id = list(
                Program.objects.values_list('id', flat=True))

        five_query = FiveW.objects.filter(program_id__in=program_filter_id)
        if five_query.exists():
            total_budget_sum = five_query.aggregate(Sum('allocated_budget'))[
                'allocated_budget__sum']
            percentage_one = int((total_budget_sum * threshold) / 100)
        else:
            percentage_one = 0
        program = five_query.values('program_id__name', 'program_id', "program_id__code").exclude(
            allocated_budget__lt=percentage_one).filter(
            program_id__in=program_filter_id).distinct('program_id')

        for p in program:
            print('program_name', p['program_id__name'])
            node.append({
                'name': p['program_id__name'],
                'type': 'program',
            })
            indexes.append(p['program_id__name'] + str(p['program_id__code']))
            program_id.append(p['program_id'])
        component = five_query.values('component_id__name', 'component_id', 'component_id__code').exclude(
            allocated_budget__lt=percentage_one).filter(
            program_id__in=program_filter_id).distinct(
            'component_id')
        for c in component:
            node.append({
                'name': c['component_id__name'],
                'type': 'component',
            })
            indexes.append(c['component_id__name'] +
                           str(c['component_id__code']))
            component_id.append(c['component_id'])
        partner = five_query.values('supplier_id__name', 'supplier_id', "supplier_id__code").exclude(
            allocated_budget__lt=percentage_one).filter(
            program_id__in=program_filter_id).distinct('supplier_id')
        for part in partner:
            node.append({
                'name': part['supplier_id__name'],
                'type': 'partner',
            })
            indexes.append(part['supplier_id__name'] +
                           str(part['supplier_id__code']))
            partner_id.append(part['supplier_id'])

        # allocated_sum = query.aggregate(Sum('allocated_budget'))
        # nodes = list(query) + list(comp) + list(part)
        for i in range(0, len(component_id)):
            q = five_query.values('id', 'component_id__name', 'component_id', 'component_id__code',
                                  'program_id__name',
                                  'program_id__code',
                                  'allocated_budget').exclude(allocated_budget__lt=percentage_one).filter(
                component_id=component_id[i])

            budget = q.aggregate(Sum('allocated_budget'))
            source = indexes.index(
                q[0]['program_id__name'] + str(q[0]['program_id__code']))
            target = indexes.index(
                q[0]['component_id__name'] + str(q[0]['component_id__code']))
            links.append({
                'source': source,
                'target': target,
                'value': budget['allocated_budget__sum'],
            })

        for i in range(0, len(component_id)):
            q = five_query.values('component_id__name', 'supplier_id', 'component_id__code',
                                  'supplier_id__name',
                                  'supplier_id__code',
                                  'allocated_budget').exclude(allocated_budget__lt=percentage_one).filter(
                supplier_id__in=partner_id,
                component_id=component_id[
                    i])

            budget = q.aggregate(Sum('allocated_budget'))
            source = indexes.index(
                q[0]['component_id__name'] + str(q[0]['component_id__code']))
            target = indexes.index(
                q[0]['supplier_id__name'] + str(q[0]['supplier_id__code']))
            links.append({
                'source': source,
                'target': target,
                'value': budget['allocated_budget__sum'],
            })

        return Response({"minThreshold": percentage_one, "nodes": node, "links": links})


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
        count = []

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
            province_filter_id = list(Province.objects.exclude(
                code=-1).values_list('id', flat=True).distinct())

        if request.GET.getlist('program'):
            prov = request.GET['program']
            program = prov.split(",")
            for i in range(0, len(program)):
                program[i] = int(program[i])
        else:
            program = list(Program.objects.values_list('id', flat=True))
            count.append('program')

        if request.GET.getlist('sector_id'):
            sect = request.GET['sector_id']
            sector = sect.split(",")
            for i in range(0, len(sector)):
                sector[i] = int(sector[i])
        else:
            sector = list(Sector.objects.values_list('id', flat=True))
            count.append('sector')

        if request.GET.getlist('sub_sector_id'):
            subsect = request.GET['sub_sector_id']
            sub_sector = subsect.split(",")
            for i in range(0, len(sub_sector)):
                sub_sector[i] = int(sub_sector[i])
        else:
            sub_sector = list(Sector.objects.values_list('id', flat=True))
            count.append('sub_sector')
        if request.GET.getlist('marker_category_id'):
            mc = request.GET['marker_category_id']
            markers = mc.split(",")
            for i in range(0, len(markers)):
                markers[i] = int(markers[i])
        else:
            markers = list(MarkerCategory.objects.values_list('id', flat=True))
            count.append('markers')

        if request.GET.getlist('marker_value_id'):
            mv = request.GET['marker_value_id']
            markers_value = mv.split(",")
            for i in range(0, len(markers_value)):
                markers_value[i] = int(markers_value[i])
        else:
            markers_value = list(
                MarkerValues.objects.values_list('id', flat=True))
            count.append('markers_value')

        if request.GET.getlist('supplier_id'):
            supp = request.GET['supplier_id']
            supplier = supp.split(",")
            for i in range(0, len(supplier)):
                supplier[i] = int(supplier[i])
        else:
            supplier = list(Partner.objects.values_list('id', flat=True))
            count.append('supplier')

        if request.GET.getlist('component_code'):
            comp = request.GET['component_code']
            component = comp.split(",")
            for i in range(0, len(component)):
                component[i] = str(component[i])
        else:
            component = list(Project.objects.values_list('code', flat=True))
            count.append('component')

        five_query = sankey(province_filter_id, supplier, program, component, sector, sub_sector, markers,
                            markers_value, count)
        print(five_query)
        if five_query.exists():
            total_budget_sum = five_query.aggregate(Sum('allocated_budget'))[
                'allocated_budget__sum']

            percentage_one = int((total_budget_sum * threshold) / 100)
        else:
            percentage_one = 0
        province = five_query.values('province_id__name', 'province_id', "province_id__code").distinct(
            'province_id').exclude(allocated_budget__lt=percentage_one)
        for p in province:
            node.append({
                'name': p['province_id__name'],
                'type': 'province',
            })
            indexes.append(p['province_id__name'] +
                           str(p['province_id__code']))
            province_id.append(p['province_id'])
        district = five_query.values('province_id', 'district_id__name', 'district_id',
                                     'district_id__code').distinct(
            'district_id').exclude(allocated_budget__lt=percentage_one).filter(~Q(district_id__code=-1))
        for c in district:
            node.append({
                'name': c['district_id__name'],
                'type': 'district',
            })
            indexes.append(c['district_id__name'] +
                           str(c['district_id__code']))
            district_id.append(c['district_id'])
        municipality = five_query.values('province_id', 'municipality_id__name', 'municipality_id',
                                         "municipality_id__code").distinct('municipality_id').exclude(
            allocated_budget__lt=percentage_one).filter(~Q(municipality_id__code=-1))
        for part in municipality:
            node.append({
                'name': part['municipality_id__name'],
                'type': 'municipality',
            })
            indexes.append(part['municipality_id__name'] +
                           str(part['municipality_id__code']))
            municipality_id.append(part['municipality_id'])
        for i in range(0, len(district_id)):
            q = five_query.values('district_id__name', 'district_id', 'district_id__code',
                                  'province_id__name',
                                  'province_id__code',
                                  'allocated_budget').filter(district_id=district_id[i]).exclude(
                allocated_budget__lt=percentage_one)

            budget = q.aggregate(Sum('allocated_budget'))
            source = indexes.index(
                q[0]['province_id__name'] + str(q[0]['province_id__code']))
            target = indexes.index(
                q[0]['district_id__name'] + str(q[0]['district_id__code']))
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
            source = indexes.index(
                q[0]['district_id__name'] + str(q[0]['district_id__code']))
            target = indexes.index(
                q[0]['municipality_id__name'] + str(q[0]['municipality_id__code']))
            links.append({
                'source': source,
                'target': target,
                'value': budget['allocated_budget__sum'],
            })

        return Response({"minThreshold": percentage_one, "nodes": node, "links": links})


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


class FAQView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order']

    def get_queryset(self):
        queryset = FAQ.objects.order_by('order')
        return queryset

    def get_serializer_class(self):
        serializer_class = FAQSerializer
        return serializer_class


class NationalStatisticView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = NationalStatistic.objects.order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = NetionalStatisticSerializer
        return serializer_class


class TermsAndConditionView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']

    def get_queryset(self):
        queryset = TermsAndCondition.objects.order_by('order')
        return queryset

    def get_serializer_class(self):
        serializer_class = TermsAndConditionSerializer
        return serializer_class


class ManualViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Manual.objects.order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = ManualSerializer
        return serializer_class


class ProgramProfile(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = FiveW.objects.all()
    serializer_class = FivewSerializer

    def list(self, request, *args, **kwargs):
        data = []
        activemap = []
        if request.GET.getlist('region') and request.GET.getlist('program_id'):
            if request.GET['region'] == 'province':
                programid = request.GET['program_id']
                fivew = FiveW.objects.filter(program_id=programid).values('id', "allocated_budget", 'province_id',
                                                                          'district_id',
                                                                          'municipality_id', 'component_id__name',
                                                                          'province_id__name',
                                                                          'province_id__code').distinct()
                fivew = fivew.exclude(
                    municipality_id__code='-1',
                    district_id__code='-1',
                    province_id__code='-1')
                for f in fivew:
                    if f['province_id'] is not None:
                        data.append(f['component_id__name'])

                for t in fivew.distinct('province_id'):
                    acti = {
                        'code': t['province_id__code'],
                        'name': t['province_id__name']
                    }
                    activemap.append(acti)

                def unique(list1):
                    unique_list = []
                    finaldata = []
                    for x in list1:
                        if x not in unique_list:
                            unique_list.append(x)
                    for x in unique_list:
                        finaldata.append(x)
                    if None in finaldata:
                        finaldata.remove(None)
                    return finaldata

                finaldata = unique(data)

                total_budget = fivew.aggregate(Sum('allocated_budget'))
                province_count = fivew.distinct('province_id').count()
                district_count = fivew.distinct('district_id').count()
                municipality_count = fivew.distinct('municipality_id').count()
                program = Program.objects.get(id=programid)
                return Response(
                    {"program_name": program.name, "start_date": program.start_date, "end_date": program.end_date,
                     "description": program.description,
                     "total_budget": program.total_budget, "province_count": province_count,
                     "district_count": district_count, "municiaplity_count": municipality_count,
                     'federal_level_components': finaldata, 'activemap': activemap})
            elif request.GET['region'] == 'district':
                programid = request.GET['program_id']
                fivew = FiveW.objects.filter(program_id=programid).values('id', "allocated_budget", 'province_id',
                                                                          'district_id',
                                                                          'municipality_id', 'component_id__name',
                                                                          'district_id__name',
                                                                          'district_id__code').distinct()
                fivew = fivew.exclude(
                    municipality_id__code='-1',
                    district_id__code='-1',
                    province_id__code='-1')
                for f in fivew:
                    if f['district_id'] is not None:
                        data.append(f['component_id__name'])

                for t in fivew.distinct('district_id'):
                    acti = {
                        'code': t['district_id__code'],
                        'name': t['district_id__name']
                    }
                    activemap.append(acti)

                def unique(list1):
                    unique_list = []
                    finaldata = []
                    for x in list1:
                        if x not in unique_list:
                            unique_list.append(x)
                    for x in unique_list:
                        finaldata.append(x)
                    if None in finaldata:
                        finaldata.remove(None)
                    return finaldata

                finaldata = unique(data)

                total_budget = fivew.aggregate(Sum('allocated_budget'))
                province_count = fivew.distinct('province_id').count()
                district_count = fivew.distinct('district_id').count()
                municipality_count = fivew.distinct('municipality_id').count()
                program = Program.objects.get(id=programid)
                return Response(
                    {"program_name": program.name, "start_date": program.start_date, "end_date": program.end_date,
                     "description": program.description,
                     "total_budget": total_budget['allocated_budget__sum'], "province_count": province_count,
                     "district_count": district_count, "municiaplity_count": municipality_count,
                     'federal_level_components': finaldata, 'activemap': activemap})
            elif request.GET['region'] == 'municipality':
                programid = request.GET['program_id']
                fivew = FiveW.objects.filter(program_id=programid).values('id', "allocated_budget", 'province_id',
                                                                          'district_id',
                                                                          'municipality_id', 'component_id__name',
                                                                          'municipality_id__name',
                                                                          'municipality_id__code').distinct()

                fivew = fivew.exclude(
                    municipality_id__code='-1',
                    district_id__code='-1',
                    province_id__code='-1')

                for f in fivew:
                    if f['municipality_id'] is not None:
                        data.append(f['component_id__name'])

                for t in fivew.distinct('municipality_id'):
                    acti = {
                        'code': t['municipality_id__code'],
                        'name': t['municipality_id__name']
                    }
                    activemap.append(acti)

                def unique(list1):
                    unique_list = []
                    finaldata = []
                    for x in list1:
                        if x not in unique_list:
                            unique_list.append(x)
                    for x in unique_list:
                        finaldata.append(x)
                    if None in finaldata:
                        finaldata.remove(None)
                    return finaldata

                finaldata = unique(data)

                total_budget = fivew.aggregate(Sum('allocated_budget'))
                province_count = fivew.distinct('province_id').count()
                district_count = fivew.distinct('district_id').count()
                municipality_count = fivew.distinct('municipality_id').count()
                program = Program.objects.get(id=programid)
                return Response(
                    {"program_name": program.name, "start_date": program.start_date, "end_date": program.end_date,
                     "description": program.description,
                     "total_budget": total_budget['allocated_budget__sum'], "province_count": province_count,
                     "district_count": district_count, "municiaplity_count": municipality_count,
                     'federal_level_components': finaldata, 'activemap': activemap})
            else:
                return Response({"results": "please pass region"})
        else:
            return Response({"results": "Please Pass Full Params"})


class RegionalProfile(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = FiveW.objects.all()
    serializer_class = FivewSerializer

    def list(self, request, *args, **kwargs):
        if request.GET['region'] == 'province':
            data = []
            sector_ids = []
            sector_by_buget = []
            program_ids = []
            top_prog_by_budget = []
            supplier_ids = []
            top_part_by_budget = []
            top_sector_by_no_partner = []
            fivew_data = []
            addition_type = ['meters', 'count', 'sqkm']
            average_type = ['percent', 'millimeters / month',
                            'persons per household', 'indices', 'hour']
            if 'province_code' in request.GET:
                ind = Indicator.objects.filter(federal_level__in=['province', 'all']).exclude(
                    Q(show_flag=False) | Q(is_dashboard=False) | Q(is_regional_profile=False)).values(
                    'category', 'id',
                    'federal_level',
                    'full_title',
                    'indicator').distinct()

                for d in ind:
                    if d['federal_level'] == 'province':
                        initial_sum = 0
                        test = IndicatorValue.objects.filter(indicator_id__id=d['id'],
                                                             province_id__code=int(
                                                                 request.GET['province_code'])).values('value')
                        for test in test:
                            initial_sum += test['value']
                        data.append({
                            'code': int(request.GET['province_code']),
                            'indicator_id': d['id'],
                            'category': d['category'],
                            'indicator': d['full_title'],
                            'value': initial_sum
                        })
                    else:
                        test = IndicatorValue.objects.filter(indicator_id__id=d['id'],
                                                             gapanapa_id__province_id__code=int(
                                                                 request.GET['province_code'])).values('value',
                                                                                                       'indicator_id__unit')

                        count = 0
                        value_sum = 0
                        for ind in test:
                            if ind['indicator_id__unit'] in addition_type:
                                if math.isnan(ind['value']) == False:
                                    value_sum = (value_sum + ind['value'])
                                else:
                                    value_sum = (value_sum + 0)
                            elif ind['indicator_id__unit'] in average_type:
                                if math.isnan(ind['value']) == False:
                                    count += 1
                                    value_sum = (value_sum + ind['value'])
                                else:
                                    count += 1
                                    value_sum = (value_sum + 0)
                        try:
                            if test[0]['indicator_id__unit'] in average_type:
                                value_sum = value_sum / count
                        except:
                            pass
                        data.append({
                            'code': int(request.GET['province_code']),
                            'indicator_id': d['id'],
                            'category': d['category'],
                            'indicator': d['full_title'],
                            'value': value_sum
                        })
                five = FiveW.objects.filter(province_id__code=int(request.GET['province_code'])).values(
                    'id',
                    'allocated_budget',
                    'program_id__sector__name',
                    'program_id__sector__id',
                    'program_id',
                    'supplier_id',
                    'allocated_budget',
                    'province_id__code'
                ).distinct()
                for f in five:
                    sector_ids.append(f['program_id__sector__id'])
                    program_ids.append(f['program_id'])
                    supplier_ids.append(f['supplier_id'])

                def unique(list1):
                    # Returns Unique Value form a list
                    unique_list = []
                    finaldata = []
                    for x in list1:
                        if x not in unique_list:
                            unique_list.append(x)
                    for x in unique_list:
                        finaldata.append(x)
                    if None in finaldata:
                        finaldata.remove(None)
                    return finaldata

                uniqueprogramid = unique(program_ids)
                supplieruniqueid = unique(supplier_ids)
                if len(supplieruniqueid) != 0:
                    for l in supplieruniqueid:
                        total_partner_budget = 0
                        partner = Partner.objects.filter(
                            id=int(l)).values('name')
                        fivenew = FiveW.objects.filter(supplier_id=l,
                                                       province_id__code=int(request.GET['province_code'])).values(
                            'supplier_id__name', 'supplier_id',
                            'allocated_budget')
                        for f in fivenew:
                            total_partner_budget += f['allocated_budget']
                        top_part_by_budget.append({
                            'id': l,
                            'name': partner[0]['name'],
                            'key': 'total_budget',
                            'value': total_partner_budget
                        })
                if len(uniqueprogramid) != 0:
                    for p in uniqueprogramid:
                        pr = FiveW.objects.filter(program_id=p,
                                                  province_id__code=int(request.GET['province_code'])).exclude(
                            allocated_budget=None).values('allocated_budget', 'program_id__name',
                                                          'program_id__id', 'program_id__program_acronym')
                        top_prog_by_budget.append({
                            'id': pr[0]['program_id__id'],
                            'name': pr[0]['program_id__name'],
                            'acronym': pr[0]['program_id__program_acronym'],
                            'key': 'total_budget',
                            'value': pr.aggregate(Sum('allocated_budget'))['allocated_budget__sum']
                        })
                test2 = sorted(top_prog_by_budget,
                               key=lambda i: i['value'], reverse=True)
                test3 = sorted(top_part_by_budget,
                               key=lambda i: i['value'], reverse=True)
                total_budget = five.aggregate(Sum('allocated_budget'))[
                    'allocated_budget__sum']
                sector_count = five.distinct('program_id__sector').exclude(
                    program_id__sector=None).count()
                program_count = five.distinct('program_id').count()
                component_count = five.distinct('component_id').count()
                supplier_count = five.distinct('supplier_id').count()
                fivew_data.append({
                    'total_budget': total_budget,
                    'sector_count': sector_count,
                    'program_count': program_count,
                    'component_count': component_count,
                    'supplier_count': supplier_count
                })
                return Response({"indicatordata": data, 'fivewdata': fivew_data,
                                 'top_program_by_budget': test2,
                                 'top_partner_by_budget': test3})
            else:
                return Response({"results": "Please Pass Province Code"})

        elif request.GET['region'] == 'district':
            data = []
            sector_ids = []
            program_ids = []
            top_prog_by_budget = []
            top_part_by_budget = []
            supplier_ids = []
            fivew_data = []
            addition_type = ['meters', 'count', 'sqkm']
            average_type = ['percent', 'millimeters / month',
                            'persons per household', 'indices', 'hour']
            if 'district_code' in request.GET:
                ind = Indicator.objects.filter(federal_level__in=['district', 'all']).exclude(
                    Q(show_flag=False) | Q(is_dashboard=False) | Q(is_regional_profile=False)).values(
                    'category', 'id',
                    'federal_level',
                    'indicator',
                    'full_title').distinct()
                for d in ind:
                    if d['federal_level'] == 'district':
                        initial_sum = 0
                        test = IndicatorValue.objects.filter(indicator_id__id=d['id'],
                                                             district_id__code=int(
                                                                 request.GET['district_code'])).values(
                            'value')
                        for test in test:
                            initial_sum += test['value']
                        data.append({
                            'code': int(request.GET['district_code']),
                            'indicator_id': d['id'],
                            'category': d['category'],
                            'indicator': d['full_title'],
                            'value': initial_sum
                        })
                    else:
                        print("1")
                        test = IndicatorValue.objects.filter(indicator_id__id=d['id'],
                                                             gapanapa_id__district_id__code=int(
                                                                 request.GET['district_code'])).values(
                            'value', 'indicator_id__unit')
                        count = 0
                        value_sum = 0
                        for ind in test:
                            if ind['indicator_id__unit'] in addition_type:
                                if math.isnan(ind['value']) == False:
                                    value_sum = (value_sum + ind['value'])
                                else:
                                    value_sum = (value_sum + 0)
                            elif ind['indicator_id__unit'] in average_type:
                                if math.isnan(ind['value']) == False:
                                    count += 1
                                    value_sum = (value_sum + ind['value'])
                                else:
                                    count += 1
                                    value_sum = (value_sum + 0)
                        try:
                            if test[0]['indicator_id__unit'] in average_type:
                                value_sum = value_sum / count
                        except:
                            pass
                        data.append({
                            'code': int(request.GET['district_code']),
                            'indicator_id': d['id'],
                            'category': d['category'],
                            'indicator': d['full_title'],
                            'value': value_sum
                        })
                five = FiveW.objects.filter(district_id__code=int(request.GET['district_code'])).exclude(
                    municipality_id__code='-1',
                    district_id__code='-1',
                    province_id__code='-1').values(
                    'id',
                    'allocated_budget',
                    'program_id__sector__name',
                    'program_id__sector__id',
                    'program_id', 'district_id__code',
                    'supplier_id'
                ).distinct()
                for f in five:
                    sector_ids.append(f['program_id__sector__id'])
                    program_ids.append(f['program_id'])
                    supplier_ids.append(f['supplier_id'])

                def unique(list1):
                    unique_list = []
                    finaldata = []
                    for x in list1:
                        if x not in unique_list:
                            unique_list.append(x)
                    for x in unique_list:
                        finaldata.append(x)
                    if None in finaldata:
                        finaldata.remove(None)
                    return finaldata

                uniqueprogramid = unique(program_ids)
                supplieruniqueid = unique(supplier_ids)
                if len(supplieruniqueid) != 0:
                    for l in supplieruniqueid:
                        total_partner_budget = 0
                        partner = Partner.objects.filter(
                            id=int(l)).values('name')
                        fivenew = FiveW.objects.filter(supplier_id=l,
                                                       district_id__code=int(request.GET['district_code'])).values(
                            'supplier_id__name', 'supplier_id',
                            'allocated_budget')
                        for f in fivenew:
                            total_partner_budget += f['allocated_budget']
                        top_part_by_budget.append({
                            'id': l,
                            'name': partner[0]['name'],
                            'key': 'total_budget',
                            'value': total_partner_budget
                        })
                if len(uniqueprogramid) != 0:
                    for p in uniqueprogramid:
                        pr = FiveW.objects.filter(program_id=p,
                                                  district_id__code=int(request.GET['district_code'])).exclude(
                            allocated_budget=None).values('allocated_budget', 'program_id__name',
                                                          'program_id__id', 'program_id__program_acronym')
                        top_prog_by_budget.append({
                            'id': pr[0]['program_id__id'],
                            'name': pr[0]['program_id__name'],
                            'acronym': pr[0]['program_id__program_acronym'],
                            'key': 'total_budget',
                            'value': pr.aggregate(Sum('allocated_budget'))['allocated_budget__sum']
                        })
                test2 = sorted(top_prog_by_budget,
                               key=lambda i: i['value'], reverse=True)
                test3 = sorted(top_part_by_budget,
                               key=lambda i: i['value'], reverse=True)
                total_budget = five.aggregate(Sum('allocated_budget'))[
                    'allocated_budget__sum']
                sector_count = five.distinct('program_id__sector').exclude(
                    program_id__sector=None).count()
                program_count = five.distinct('program_id').count()
                component_count = five.distinct('component_id').count()
                supplier_count = five.distinct('supplier_id').count()
                fivew_data.append({
                    'total_budget': total_budget,
                    'sector_count': sector_count,
                    'program_count': program_count,
                    'component_count': component_count,
                    'supplier_count': supplier_count
                })
                return Response({"indicatordata": data, 'fivewdata': fivew_data,
                                 'top_program_by_budget': test2,
                                 'top_partner_by_budget': test3})
            else:
                return Response({"results": "Please Pass District Code"})
        elif request.GET['region'] == 'municipality':
            data = []
            sector_ids = []
            sector_by_buget = []
            program_ids = []
            top_prog_by_budget = []
            supplier_ids = []
            top_part_by_budget = []
            top_sector_by_no_partner = []
            fivew_data = []
            if 'municipality_code' in request.GET:
                ind = Indicator.objects.filter(federal_level__in=['palika', 'all']).exclude(
                    Q(show_flag=False) | Q(is_dashboard=False) | Q(is_regional_profile=False)).values(
                    'category', 'id',
                    'federal_level',
                    'full_title',
                    'indicator').distinct()

                for d in ind:
                    initial_sum = 0
                    test = IndicatorValue.objects.filter(indicator_id__id=d['id'],
                                                         gapanapa_id__code=int(
                                                             request.GET['municipality_code'])).values('indicator_id',
                                                                                                       'value')
                    print(test)
                    for test in test:
                        initial_sum += test['value']
                    data.append({
                        'code': int(request.GET['municipality_code']),
                        'indicator_id': d['id'],
                        'category': d['category'],
                        'indicator': d['full_title'],
                        'value': initial_sum
                    })
                five = FiveW.objects.filter(municipality_id__code=int(request.GET['municipality_code'])).exclude(
                    municipality_id__code='-1',
                    district_id__code='-1',
                    province_id__code='-1').values(
                    'id',
                    'allocated_budget',
                    'program_id__sector__name',
                    'program_id__sector__id',
                    'program_id', 'municipality_id__code', 'supplier_id').distinct()

                for f in five:
                    sector_ids.append(f['program_id__sector__id'])
                    program_ids.append(f['program_id'])
                    supplier_ids.append(f['supplier_id'])

                def unique(list1):
                    unique_list = []
                    finaldata = []
                    for x in list1:
                        if x not in unique_list:
                            unique_list.append(x)
                    for x in unique_list:
                        finaldata.append(x)
                    if None in finaldata:
                        finaldata.remove(None)
                    return finaldata

                uniqueprogramid = unique(program_ids)
                supplieruniqueid = unique(supplier_ids)
                if len(supplieruniqueid) != 0:
                    for l in supplieruniqueid:
                        total_partner_budget = 0
                        partner = Partner.objects.filter(
                            id=int(l)).values('name')
                        fivenew = FiveW.objects.filter(supplier_id=l, municipality_id__code=int(
                            request.GET['municipality_code'])).values('supplier_id__name', 'supplier_id',
                                                                      'allocated_budget')
                        for f in fivenew:
                            total_partner_budget += f['allocated_budget']
                        top_part_by_budget.append({
                            'id': l,
                            'name': partner[0]['name'],
                            'key': 'total_budget',
                            'value': total_partner_budget
                        })
                if len(uniqueprogramid) != 0:
                    for p in uniqueprogramid:
                        pr = FiveW.objects.filter(program_id=p,
                                                  municipality_id__code=int(request.GET['municipality_code'])).exclude(
                            allocated_budget=None).values('allocated_budget', 'program_id__name',
                                                          'program_id__id', 'program_id__program_acronym')
                        top_prog_by_budget.append({
                            'id': pr[0]['program_id__id'],
                            'name': pr[0]['program_id__name'],
                            'acronym': pr[0]['program_id__program_acronym'],
                            'key': 'total_budget',
                            'value': pr.aggregate(Sum('allocated_budget'))['allocated_budget__sum']
                        })
                test2 = sorted(top_prog_by_budget,
                               key=lambda i: i['value'], reverse=True)
                test3 = sorted(top_part_by_budget,
                               key=lambda i: i['value'], reverse=True)
                total_budget = five.aggregate(Sum('allocated_budget'))[
                    'allocated_budget__sum']
                sector_count = five.distinct('program_id__sector').exclude(
                    program_id__sector=None).count()
                program_count = five.distinct('program_id').count()
                component_count = five.distinct('component_id').count()
                supplier_count = five.distinct('supplier_id').count()
                fivew_data.append({
                    'total_budget': total_budget,
                    'sector_count': sector_count,
                    'program_count': program_count,
                    'component_count': component_count,
                    'supplier_count': supplier_count
                })
                return Response({"indicatordata": data, 'fivewdata': fivew_data,
                                 'top_program_by_budget': test2,
                                 'top_partner_by_budget': test3})
            else:
                return Response({"results": "Please Pass Municipality Code"})
        else:
            return Response({"results": "Invalid Region"})


class ProgramUpperDendrogram(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = FiveW.objects.all()
    serializer_class = FivewSerializer

    def list(self, request, *args, **kwargs):
        if request.GET.getlist('program_id'):
            component = []
            programid = request.GET['program_id']
            dami = Project.objects.filter(
                program_id=programid).values('name').distinct()
            for d in dami:
                partner = []
                if d['name'] not in component:
                    component.append({
                        'name': d['name'],
                        'children': partner
                    })
                nadami = Project.objects.filter(name=d['name']).values(
                    'partner_id__name').distinct()
                for n in nadami:
                    if n['partner_id__name'] not in partner:
                        partner.append({
                            'name': n['partner_id__name']
                        })
            return Response({"results": component})
        else:
            return Response({"results": "Please Pass program_id"})


class ProgramLowerDendrogram(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = FiveW.objects.all()
    serializer_class = FivewSerializer

    def list(self, request, *args, **kwargs):
        if request.GET.getlist('program_id'):
            component = []
            programid = request.GET['program_id']
            dami = Project.objects.filter(
                program_id=programid).values('name').distinct()
            print(dami)
            for d in dami:
                province = []
                if d['name'] not in component:
                    component.append({
                        'name': d['name'],
                        'children': province
                    })
                nadami = FiveW.objects.filter(component_id__name=d['name']).exclude(
                    municipality_id__code='-1',
                    district_id__code='-1',
                    province_id__code='-1'
                ).values(
                    'province_id__name', 'province_id__code').distinct()
                for n in nadami:
                    district = []
                    if n['province_id__name'] not in province:
                        province.append({
                            'name': n['province_id__name'],
                            'code': n['province_id__code'],
                            'children': district
                        })
                    dist = FiveW.objects.filter(province_id__name=n['province_id__name'],
                                                component_id__name=d['name']).exclude(
                        municipality_id__code='-1',
                        district_id__code='-1',
                        province_id__code='-1'
                    ).values('district_id__name', 'district_id__code').distinct()

                    for x in dist:
                        if x['district_id__code'] != '-1':
                            if x['district_id__name'] not in district:
                                district.append({
                                    'name': x['district_id__name'],
                                    'code': x['district_id__code']
                                })
            return Response({"results": component})
        else:
            return Response({"results": "Please Pass program_id"})


class RegionalDendrogram(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = FiveW.objects.all()
    serializer_class = FivewSerializer

    def list(self, request, *args, **kwargs):
        program = []
        if request.GET['region'] == 'province':
            if request.GET.getlist('province_code'):
                fiveprogram = FiveW.objects.filter(province_id__code=request.GET['province_code']).exclude(
                    municipality_id__code='-1',
                    district_id__code='-1',
                    province_id__code='-1').values(
                    'program_id__name').distinct()
                for f in fiveprogram:
                    component = []
                    dami = FiveW.objects.filter(program_id__name=f['program_id__name'],
                                                province_id__code=request.GET['province_code']).values(
                        'component_id__name').distinct()
                    program.append({
                        "name": f['program_id__name'],
                        "children": component
                    })
                    for d in dami:
                        partner = []
                        if d['component_id__name'] not in component:
                            component.append({
                                'name': d['component_id__name'],
                                'children': partner
                            })
                        nadami = FiveW.objects.filter(component_id__name=d['component_id__name'],
                                                      province_id__code=request.GET['province_code']).values(
                            'supplier_id__name').distinct()
                        for n in nadami:
                            if n['supplier_id__name'] not in partner:
                                partner.append({
                                    'name': n['supplier_id__name']
                                })
            else:
                return Response({"results": "Please Pass Province Code"})
            return Response({"results": program})
        elif request.GET['region'] == 'district':
            if request.GET.getlist('district_code'):
                fiveprogram = FiveW.objects.filter(district_id__code=request.GET['district_code']).exclude(
                    municipality_id__code='-1',
                    district_id__code='-1',
                    province_id__code='-1').values(
                    'program_id__name').distinct()
                for f in fiveprogram:
                    component = []
                    dami = FiveW.objects.filter(program_id__name=f['program_id__name'],
                                                district_id__code=request.GET['district_code']).values(
                        'component_id__name').distinct()
                    program.append({
                        "name": f['program_id__name'],
                        "children": component
                    })
                    for d in dami:
                        partner = []
                        if d['component_id__name'] not in component:
                            component.append({
                                'name': d['component_id__name'],
                                'children': partner
                            })
                        nadami = FiveW.objects.filter(component_id__name=d['component_id__name'],
                                                      district_id__code=request.GET['district_code']).values(
                            'supplier_id__name').distinct()
                        print(nadami)
                        for n in nadami:
                            if n['supplier_id__name'] not in partner:
                                partner.append({
                                    'name': n['supplier_id__name']
                                })
            else:
                return Response({"results": "Please Pass District Code"})
            return Response({"results": program})
        elif request.GET['region'] == 'municipality':
            if request.GET.getlist('municipality_code'):
                fiveprogram = FiveW.objects.filter(municipality_id__code=request.GET['municipality_code']).exclude(
                    municipality_id__code='-1',
                    district_id__code='-1',
                    province_id__code='-1').values(
                    'program_id__name').distinct()
                for f in fiveprogram:
                    component = []
                    dami = FiveW.objects.filter(program_id__name=f['program_id__name'],
                                                municipality_id__code=request.GET['municipality_code']).values(
                        'component_id__name').distinct()
                    print(dami)
                    program.append({
                        "name": f['program_id__name'],
                        "children": component
                    })
                    for d in dami:
                        partner = []
                        if d['component_id__name'] not in component:
                            component.append({
                                'name': d['component_id__name'],
                                'children': partner
                            })
                        nadami = FiveW.objects.filter(component_id__name=d['component_id__name'],
                                                      municipality_id__code=request.GET['municipality_code']).values(
                            'supplier_id__name').distinct()
                        print(nadami)
                        for n in nadami:
                            if n['supplier_id__name'] not in partner:
                                partner.append({
                                    'name': n['supplier_id__name']
                                })
            else:
                return Response({"results": "Please Pass Municipality Code"})
            return Response({"results": program})
        else:
            return Response({"results": "Invalid Region"})


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
    queryset = IndicatorValue.objects.all()
    serializer_class = DistrictSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'indicator_id', ]

    def list(self, request, **kwargs):
        """
            *required= id of indicator as param{indicator_id} send as get request - /district-indicator/?indicator_id={indicator_id}
            """
        data = []
        if self.request.GET.getlist('province_id'):
            province = self.request.GET['province_id']
            province_ids = province.split(",")
            for i in range(0, len(province_ids)):
                province_ids[i] = int(province_ids[i])
        else:
            province_ids = Province.objects.values_list('id', flat=True)

        district = District.objects.filter(province_id__id__in=province_ids).values('name', 'id', 'n_code',
                                                                                    'code').exclude(
            code=-1).order_by('id')
        id_indicators = request.GET['indicator_id']
        id_indicator = id_indicators.split(",")
        for i in range(0, len(id_indicator)):
            id_indicator[i] = int(id_indicator[i])
        for i in range(0, len(id_indicator)):
            cat_in = Indicator.objects.get(id=int(id_indicator[i]))
            if cat_in.federal_level == 'district':
                indicator_dist = IndicatorValue.objects.values('id', 'indicator_id', 'value',
                                                               'district_id__code').filter(
                    indicator_id=id_indicator[i], dsitrict_id__province_id__id__in=province_ids)

                for dist_ind in indicator_dist:
                    data.append(
                        {
                            'id': dist_ind['id'],
                            'indicator_id': int(id_indicator[i]),
                            'code': dist_ind['district_id__code'],
                            'value': dist_ind['value']

                        }
                    )
            else:
                for dist in district:
                    addition_type = ['meters', 'count', 'sqkm']
                    average_type = ['percent', 'millimeters / month',
                                    'persons per household', 'indices']
                    indicator = IndicatorValue.objects.values('id', 'indicator_id', 'value',
                                                              'indicator_id__unit').filter(
                        indicator_id=int(id_indicator[i]),
                        gapanapa_id__district_id=dist['id'])
                    value_sum = 0
                    count = 0
                    for ind in indicator:
                        if ind['indicator_id__unit'] in addition_type:
                            if math.isnan(ind['value']) == False:
                                value_sum = (value_sum + ind['value'])
                            else:
                                value_sum = (value_sum + 0)
                        elif ind['indicator_id__unit'] in average_type:
                            if math.isnan(ind['value']) == False:
                                count += 1
                                value_sum = (value_sum + ind['value'])
                            else:
                                count += 1
                                value_sum = (value_sum + 0)
                    if indicator:
                        if indicator.first()['indicator_id__unit'] in average_type:
                            value_sum = value_sum / count

                    data.append(
                        {
                            'id': dist['id'],
                            'indicator_id': int(id_indicator[i]),
                            'code': dist['code'],
                            'value': value_sum

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
        addition_type = ['meters', 'count', 'sqkm']
        average_type = ['percent', 'millimeters / month',
                        'persons per household', 'indices']
        province = Province.objects.values(
            'name', 'id', 'code').exclude(code=-1).order_by('id')
        id_indicators = request.GET['indicator_id']
        id_indicator = id_indicators.split(",")
        for i in range(0, len(id_indicator)):
            id_indicator[i] = int(id_indicator[i])
        for i in range(0, len(id_indicator)):
            for dist in province:
                value_sum = 0
                indicator = IndicatorValue.objects.values('id', 'indicator_id', 'value',
                                                          'gapanapa_id__population', 'indicator_id__unit').filter(
                    indicator_id=int(id_indicator[i]),
                    gapanapa_id__province_id=dist['id'])
                count = 0
                for ind in indicator:
                    if ind['indicator_id__unit'] in addition_type:
                        if math.isnan(ind['value']) == False:
                            value_sum = (value_sum + ind['value'])
                        else:
                            value_sum = (value_sum + 0)
                    elif ind['indicator_id__unit'] in average_type:
                        if math.isnan(ind['value']) == False:
                            count += 1
                            value_sum = (value_sum + ind['value'])
                        else:
                            count += 1
                            value_sum = (value_sum + 0)
                if indicator:
                    if indicator.first()['indicator_id__unit'] in average_type:
                        value_sum = value_sum / count

                data.append(
                    {
                        'id': dist['id'],
                        'indicator_id': int(id_indicator[i]),
                        'code': dist['code'],
                        'value': value_sum

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
        queryset = MarkerValues.objects.select_related(
            'marker_category_id').order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = MarkerValuesSerializer
        return serializer_class


class DistrictApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'province_id', 'code']

    def get_queryset(self):
        queryset = District.objects.exclude(code=-1).order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = DistrictSerializer
        return serializer_class


class ProvinceApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'code']

    def get_queryset(self):
        queryset = Province.objects.exclude(code=-1).order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = ProvinceSerializer
        return serializer_class


class GapaNapaApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'province_id', 'district_id',
                        'hlcit_code', 'gn_type_en', 'gn_type_np', 'code']
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
    queryset = FiveW.objects.all()
    serializer_class = FivewSerializer

    def list(self, request, *args, **kwargs):
        data = []
        count = []
        if request.GET.getlist('sector_id'):
            sect = request.GET['sector_id']
            sector = sect.split(",")
            for i in range(0, len(sector)):
                sector[i] = int(sector[i])
        else:
            sector = list(Sector.objects.values_list('id', flat=True))
            count.append('sector')
        if request.GET.getlist('sub_sector_id'):
            subsect = request.GET['sub_sector_id']
            sub_sector = subsect.split(",")
            for i in range(0, len(sub_sector)):
                sub_sector[i] = int(sub_sector[i])
        else:
            sub_sector = list(Sector.objects.values_list('id', flat=True))
            count.append('sub_sector')

        if request.GET.getlist('program_id'):
            prov = request.GET['program_id']
            program = prov.split(",")
            for i in range(0, len(program)):
                program[i] = int(program[i])
        else:
            program = list(Program.objects.values_list('id', flat=True))
            count.append('program')

        if request.GET.getlist('status'):
            st = request.GET['status']
            stat = st.split(",")
            for i in range(0, len(stat)):
                stat[i] = str(stat[i]).lower()
        else:
            stat = list(FiveW.objects.values_list('status', flat=True))
            count.append('stat')

        if request.GET.getlist('marker_category_id'):
            mc = request.GET['marker_category_id']
            markers = mc.split(",")
            for i in range(0, len(markers)):
                markers[i] = int(markers[i])
        else:
            markers = list(MarkerCategory.objects.values_list('id', flat=True))
            count.append('markers')

        if request.GET.getlist('marker_value_id'):
            mv = request.GET['marker_value_id']
            markers_value = mv.split(",")
            for i in range(0, len(markers_value)):
                markers_value[i] = int(markers_value[i])
        else:
            markers_value = list(
                MarkerValues.objects.values_list('id', flat=True))
            count.append('markers_value')

        if request.GET.getlist('supplier_id'):
            supp = request.GET['supplier_id']
            supplier = supp.split(",")
            for i in range(0, len(supplier)):
                supplier[i] = int(supplier[i])
        else:
            supplier = list(Partner.objects.values_list('id', flat=True))
            count.append('supplier')

        if request.GET.getlist('component_code'):
            comp = request.GET['component_code']
            component = comp.split(",")
            for i in range(0, len(component)):
                component[i] = str(component[i])
        else:
            component = list(Project.objects.values_list('code', flat=True))
            count.append('component')

        if request.GET.getlist('province_code'):
            province = request.GET['province_code']
            province_codes = province.split(",")
            for i in range(0, len(province_codes)):
                province_codes[i] = int(province_codes[i])
            districts = District.objects.values('name', 'id', 'code', 'n_code', 'province_id__name').filter(
                province_id__code__in=province_codes).exclude(code='-1').order_by('id')

        else:
            districts = District.objects.values(
                'name', 'id', 'code', 'n_code', 'province_id__name').order_by('id')

        for dist in districts:
            if count:
                if len(count) == 8:
                    query = FiveW.objects.filter(district_id=dist['id']).values('allocated_budget', 'component_id',
                                                                                'program_id')
                else:
                    query = fivew_district([dist['id']], supplier, program, component, sector, sub_sector, markers,
                                           markers_value, count, stat)
            else:
                query = fivew_district([dist['id']], supplier, program, component, sector, sub_sector, markers,
                                       markers_value, count, stat)

            if request.GET.getlist('field'):
                field = request.GET['field']
                value = request.GET['value']
                kwargs = {
                    '{0}__iexact'.format(field): value
                }
                query = query.filter(Q(**kwargs))

            if query:
                total_new_budget1 = 0
                prog = query.values_list(
                    'program_id__name', flat=True).distinct()
                if request.GET.getlist('sector_id'):
                    if not request.GET.getlist('sub_sector_id'):
                        da = query.values('program_id__id', 'program_id__sector_budget', 'program_id__total_budget',
                                          'allocated_budget')
                        sub_sec = [i.id for i in SubSector.objects.filter(
                            sector_id__in=sector)]
                        for d in da:
                            sec_budget = 0
                            if d['program_id__sector_budget']:
                                if d['program_id__sector_budget'] != 'None':
                                    for h in d['program_id__sector_budget'].split(','):
                                        x = h.split(':')
                                        if int(x[0]) in sub_sec:
                                            try:
                                                sec_budget += float(x[1])
                                            except:
                                                pass

                            if d['allocated_budget']:
                                print(sec_budget)
                                print(d['allocated_budget'])
                                total_new_budget1 += (d['allocated_budget']
                                                      * sec_budget) / 100
                    else:
                        da = query.values('program_id__id', 'program_id__sector_budget', 'program_id__total_budget',
                                          'allocated_budget')
                        for d in da:
                            sub_sec_budget = 0
                            if d['program_id__sector_budget']:
                                if d['program_id__sector_budget'] != 'None':
                                    for h in d['program_id__sector_budget'].split(','):
                                        x = h.split(':')
                                        if int(x[0]) in sub_sector:
                                            sub_sec_budget = float(x[1])
                            if d['allocated_budget']:
                                total_new_budget1 += (d['allocated_budget']
                                                      * sub_sec_budget) / 100
                elif request.GET.getlist('sub_sector_id'):
                    da = query.values('program_id__id', 'program_id__sector_budget', 'program_id__total_budget',
                                      'allocated_budget')
                    for d in da:
                        sub_sec_budget = 0
                        if d['program_id__sector_budget']:
                            if d['program_id__sector_budget'] != 'None':
                                for h in d['program_id__sector_budget'].split(','):
                                    x = h.split(':')
                                    if int(x[0]) in sub_sector:
                                        sub_sec_budget = float(x[1])
                        if d['allocated_budget']:
                            total_new_budget1 += (d['allocated_budget']
                                                  * sub_sec_budget) / 100

                if request.GET.getlist('sector_id'):
                    if not request.GET.getlist('sub_sector_id'):
                        budget = total_new_budget1
                    else:
                        budget = total_new_budget1
                elif request.GET.getlist('sub_sector_id'):
                    budget = total_new_budget1
                else:
                    all_budget_test = query.values('allocated_budget')
                    s = 0
                    for h in all_budget_test:
                        s += h['allocated_budget']
                    budget = s
                comp = query.values_list(
                    'component_id__name', flat=True).distinct()
                part = query.values_list(
                    'supplier_id__name', flat=True).distinct()
                sect = query.exclude(program_id__sector__name=None).values_list('program_id__sector__name',
                                                                                flat=True).distinct(
                    'program_id__sector__name')
                sub_sect = query.exclude(program_id__sub_sector__name=None).values_list(
                    'program_id__sub_sector__name',
                    flat=True).distinct()
                for s in sub_sect:
                    print(s)
                mark = query.exclude(program_id__marker_category__name=None).values_list(
                    'program_id__marker_category__name',
                    flat=True).distinct()
                mark_val = query.exclude(program_id__marker_value__value=None).values_list(
                    'program_id__marker_value__value',
                    flat=True).distinct()

            else:
                budget = 0
                prog = []
                comp = []
                part = []
                sect = []
                sub_sect = []
                mark = []
                mark_val = []

            data.append({
                'id': dist['id'],
                'name': dist['name'],
                'code': dist['code'],
                'province_name': dist['province_id__name'],
                'allocated_budget': budget,
                'program': prog,
                'component': comp,
                'partner': part,
                'sector': sect,
                'sub_sector': sub_sect,
                'marker_category': mark,
                'marker_value': mark_val

            })
        return Response({"results": data})


class FiveWProvince(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = FiveW.objects.all()
    serializer_class = FivewSerializer

    def list(self, request, *args, **kwargs):
        data = []
        count = []
        if request.GET.getlist('program_id'):
            prov = request.GET['program_id']
            program = prov.split(",")
            for i in range(0, len(program)):
                program[i] = int(program[i])
        else:
            program = list(Program.objects.values_list('id', flat=True))
            count.append('program')

        if request.GET.getlist('sector_id'):
            sect = request.GET['sector_id']
            sector = sect.split(",")
            for i in range(0, len(sector)):
                sector[i] = int(sector[i])
        else:
            sector = list(Sector.objects.values_list('id', flat=True))
            count.append('sector')

        if request.GET.getlist('sub_sector_id'):
            subsect = request.GET['sub_sector_id']
            sub_sector = subsect.split(",")
            for i in range(0, len(sub_sector)):
                sub_sector[i] = int(sub_sector[i])
        else:
            sub_sector = list(Sector.objects.values_list('id', flat=True))
            count.append('sub_sector')
        if request.GET.getlist('marker_category_id'):
            mc = request.GET['marker_category_id']
            markers = mc.split(",")
            for i in range(0, len(markers)):
                markers[i] = int(markers[i])
        else:
            markers = list(MarkerCategory.objects.values_list('id', flat=True))
            count.append('markers')

        if request.GET.getlist('status'):
            st = request.GET['status']
            stat = st.split(",")
            for i in range(0, len(stat)):
                stat[i] = str(stat[i]).lower()
        else:
            stat = list(FiveW.objects.values_list('status', flat=True))
            count.append('stat')

        if request.GET.getlist('marker_value_id'):
            mv = request.GET['marker_value_id']
            markers_value = mv.split(",")
            for i in range(0, len(markers_value)):
                markers_value[i] = int(markers_value[i])
        else:
            markers_value = list(
                MarkerValues.objects.values_list('id', flat=True))
            count.append('markers_value')

        if request.GET.getlist('supplier_id'):
            supp = request.GET['supplier_id']
            supplier = supp.split(",")
            for i in range(0, len(supplier)):
                supplier[i] = int(supplier[i])
        else:
            supplier = list(Partner.objects.values_list('id', flat=True))
            count.append('supplier')

        if request.GET.getlist('component_code'):
            comp = request.GET['component_code']
            component = comp.split(",")
            for i in range(0, len(component)):
                component[i] = str(component[i])
        else:
            component = list(Project.objects.values_list('code', flat=True))
            count.append('component')

        provinces = Province.objects.values(
            'name', 'id', 'code').order_by('id')

        for province in provinces:
            if count:
                if len(count) == 8:
                    query = FiveW.objects.filter(province_id=province['id']).values('allocated_budget', 'component_id',
                                                                                    'program_id')
                else:
                    query = fivew_province([province['id']], supplier, program, component, sector, sub_sector, markers,
                                           markers_value, count, stat)
            else:
                query = fivew_province([province['id']], supplier, program, component, sector, sub_sector, markers,
                                       markers_value, count, stat)
            if request.GET.getlist('field'):
                field = request.GET['field']
                value = request.GET['value']
                kwargs = {
                    '{0}__iexact'.format(field): value
                }
                query = query.filter(Q(**kwargs))

            if query:
                # print(len(query))
                total_new_budget1 = 0
                prog = query.values_list(
                    'program_id__name', flat=True).distinct()
                if request.GET.getlist('sector_id'):
                    if not request.GET.getlist('sub_sector_id'):
                        da = query.values('program_id__id', 'program_id__sector_budget', 'program_id__total_budget',
                                          'allocated_budget')
                        sub_sec = [i.id for i in SubSector.objects.filter(
                            sector_id__in=sector)]
                        for d in da:
                            sec_budget = 0
                            if d['program_id__sector_budget']:
                                if d['program_id__sector_budget'] != 'None':
                                    for h in d['program_id__sector_budget'].split(','):
                                        x = h.split(':')
                                        if int(x[0]) in sub_sec:
                                            try:
                                                sec_budget += float(x[1])
                                            except:
                                                pass

                            if d['allocated_budget']:
                                print(sec_budget)
                                print(d['allocated_budget'])
                                total_new_budget1 += (d['allocated_budget']
                                                      * sec_budget) / 100
                    else:
                        da = query.values('program_id__id', 'program_id__sector_budget', 'program_id__total_budget',
                                          'allocated_budget')
                        for d in da:
                            sub_sec_budget = 0
                            if d['program_id__sector_budget']:
                                if d['program_id__sector_budget'] != 'None':
                                    for h in d['program_id__sector_budget'].split(','):
                                        x = h.split(':')
                                        if int(x[0]) in sub_sector:
                                            sub_sec_budget = float(x[1])
                            if d['allocated_budget']:
                                total_new_budget1 += (d['allocated_budget']
                                                      * sub_sec_budget) / 100
                elif request.GET.getlist('sub_sector_id'):
                    da = query.values('program_id__id', 'program_id__sector_budget', 'program_id__total_budget',
                                      'allocated_budget')
                    for d in da:
                        sub_sec_budget = 0
                        if d['program_id__sector_budget']:
                            if d['program_id__sector_budget'] != 'None':
                                for h in d['program_id__sector_budget'].split(','):
                                    x = h.split(':')
                                    if int(x[0]) in sub_sector:
                                        sub_sec_budget = float(x[1])
                        if d['allocated_budget']:
                            total_new_budget1 += (d['allocated_budget']
                                                  * sub_sec_budget) / 100

                if request.GET.getlist('sector_id'):
                    if not request.GET.getlist('sub_sector_id'):
                        budget = total_new_budget1
                    else:
                        budget = total_new_budget1
                elif request.GET.getlist('sub_sector_id'):
                    budget = total_new_budget1
                else:
                    all_budget_test = query.values('allocated_budget')
                    s = 0
                    for h in all_budget_test:
                        s += h['allocated_budget']
                    budget = s
                comp = query.values_list(
                    'component_id__name', flat=True).distinct()
                part = query.values_list(
                    'supplier_id__name', flat=True).distinct()
                sect = query.exclude(program_id__sector__name=None).values_list('program_id__sector__name',
                                                                                flat=True).distinct()

                sub_sect = query.exclude(program_id__sub_sector__name=None).values_list(
                    'program_id__sub_sector__name',
                    flat=True).distinct()
                mark_cat = query.exclude(program_id__marker_category__name=None).values_list(
                    'program_id__marker_category__name', flat=True).distinct()
                mark_val = query.exclude(program_id__marker_value__value=None).values_list(
                    'program_id__marker_value__value', flat=True).distinct()

            else:
                budget = 0
                prog = []
                comp = []
                part = []
                sect = []
                sub_sect = []
                mark_cat = []
                mark_val = []

            data.append({
                'id': province['id'],
                'name': province['name'],
                'code': str(province['code']),
                'allocated_budget': budget,
                'program': prog,
                'component': comp,
                'partner': part,
                'sector': sect,
                'sub_sector': sub_sect,
                'marker_category': mark_cat,
                'marker_value': mark_val

            })
        return Response({"results": data})


class FiveWMunicipality(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = FiveW.objects.all()
    serializer_class = FivewSerializer

    def list(self, request, *args, **kwargs):
        data = []
        count = []
        if request.GET.getlist('sector_id'):
            sect = request.GET['sector_id']
            sector = sect.split(",")
            for i in range(0, len(sector)):
                sector[i] = int(sector[i])
        else:
            sector = list(Sector.objects.values_list('id', flat=True))
            count.append('sector')
        if request.GET.getlist('sub_sector_id'):
            subsect = request.GET['sub_sector_id']
            sub_sector = subsect.split(",")
            for i in range(0, len(sub_sector)):
                sub_sector[i] = int(sub_sector[i])
        else:
            sub_sector = list(Sector.objects.values_list('id', flat=True))
            count.append('sub_sector')
        if request.GET.getlist('program_id'):
            prov = request.GET['program_id']
            program = prov.split(",")
            for i in range(0, len(program)):
                program[i] = int(program[i])
        else:
            program = list(Program.objects.values_list('id', flat=True))
            count.append('program')
        if request.GET.getlist('supplier_id'):
            supp = request.GET['supplier_id']
            supplier = supp.split(",")
            for i in range(0, len(supplier)):
                supplier[i] = int(supplier[i])
        else:
            supplier = list(Partner.objects.values_list('id', flat=True))
            count.append('supplier')

        if request.GET.getlist('marker_category_id'):
            mc = request.GET['marker_category_id']
            markers = mc.split(",")
            for i in range(0, len(markers)):
                markers[i] = int(markers[i])
        else:
            markers = list(MarkerCategory.objects.values_list('id', flat=True))
            count.append('markers')

        if request.GET.getlist('marker_value_id'):
            mv = request.GET['marker_value_id']
            markers_value = mv.split(",")
            for i in range(0, len(markers_value)):
                markers_value[i] = int(markers_value[i])
        else:
            markers_value = list(
                MarkerValues.objects.values_list('id', flat=True))
            count.append('markers_value')

        if request.GET.getlist('status'):
            st = request.GET['status']
            stat = st.split(",")
            for i in range(0, len(stat)):
                stat[i] = str(stat[i]).lower()
        else:
            stat = list(FiveW.objects.values_list('status', flat=True))
            count.append('stat')

        if request.GET.getlist('component_code'):
            comp = request.GET['component_code']
            component = comp.split(",")
            for i in range(0, len(component)):
                component[i] = str(component[i])
        else:
            component = list(Project.objects.values_list('code', flat=True))
            count.append('component')

        if request.GET.getlist('province_code'):
            province = request.GET['province_code']
            province_codes = province.split(",")
            for i in range(0, len(province_codes)):
                province_codes[i] = int(province_codes[i])
            municipalities = GapaNapa.objects.values('name', 'id', 'code', 'province_id__name',
                                                     'district_id__name').filter(
                province_id__code__in=province_codes).order_by('id')

        else:
            municipalities = GapaNapa.objects.values('name', 'id', 'code', 'province_id__name',
                                                     'district_id__name').exclude(code='-1').order_by('id')

        if request.GET.getlist('district_code'):
            dist = request.GET['district_code']
            district_codes = dist.split(",")
            for i in range(0, len(district_codes)):
                district_codes[i] = int(district_codes[i])
            municipalities = GapaNapa.objects.values('name', 'id', 'code', 'province_id__name',
                                                     'district_id__name').filter(
                district_id__code__in=district_codes).exclude(code='-1').order_by('id')

        else:
            if request.GET.getlist('province_code') == []:
                municipalities = GapaNapa.objects.values('name', 'id', 'code', 'province_id__name',
                                                         'district_id__name').exclude(code='-1').order_by('id')

        for municipality in municipalities:
            if count:
                if len(count) == 8:
                    query = FiveW.objects.filter(municipality_id=municipality['id']).values('allocated_budget',
                                                                                            'component_id',
                                                                                            'program_id')
                else:
                    query = fivew_municipality([municipality['id']], supplier, program, component, sector, sub_sector,
                                               markers, markers_value, count, stat)
            else:
                query = fivew_municipality([municipality['id']], supplier, program, component, sector, sub_sector,
                                           markers, markers_value, count, stat)
            # query = FiveW.objects.values('allocated_budget', 'component_id', 'program_id').filter(
            #     municipality_id=municipality['id'],
            #     program_id__in=program, component_id__in=component, supplier_id__in=supplier,
            #     component_id__sector__id__in=sector,
            #     component_id__sub_sector__id__in=sub_sector,
            #     program_id__marker_category__id__in=markers,
            #     program_id__marker_value__id__in=markers_value
            # )

            if request.GET.getlist('field'):
                field = request.GET['field']
                value = request.GET['value']
                kwargs = {
                    '{0}__iexact'.format(field): value
                }
                query = query.filter(Q(**kwargs))

            if query.exists():
                prog = query.values_list(
                    'program_id__name', flat=True).distinct()
                total_new_budget1 = 0
                if request.GET.getlist('sector_id'):
                    if not request.GET.getlist('sub_sector_id'):
                        da = query.values('program_id__id', 'program_id__sector_budget', 'program_id__total_budget',
                                          'allocated_budget')
                        sub_sec = [i.id for i in SubSector.objects.filter(
                            sector_id__in=sector)]
                        for d in da:
                            sec_budget = 0
                            if d['program_id__sector_budget']:
                                if d['program_id__sector_budget'] != 'None':
                                    for h in d['program_id__sector_budget'].split(','):
                                        x = h.split(':')
                                        if int(x[0]) in sub_sec:
                                            try:
                                                sec_budget += float(x[1])
                                            except:
                                                pass

                            if d['allocated_budget']:
                                print(sec_budget)
                                print(d['allocated_budget'])
                                total_new_budget1 += (d['allocated_budget']
                                                      * sec_budget) / 100
                    else:
                        da = query.values('program_id__id', 'program_id__sector_budget', 'program_id__total_budget',
                                          'allocated_budget')
                        for d in da:
                            sub_sec_budget = 0
                            if d['program_id__sector_budget']:
                                if d['program_id__sector_budget'] != 'None':
                                    for h in d['program_id__sector_budget'].split(','):
                                        x = h.split(':')
                                        if int(x[0]) in sub_sector:
                                            sub_sec_budget = float(x[1])
                            if d['allocated_budget']:
                                total_new_budget1 += (d['allocated_budget']
                                                      * sub_sec_budget) / 100
                elif request.GET.getlist('sub_sector_id'):
                    da = query.values('program_id__id', 'program_id__sector_budget', 'program_id__total_budget',
                                      'allocated_budget')
                    for d in da:
                        sub_sec_budget = 0
                        if d['program_id__sector_budget']:
                            if d['program_id__sector_budget'] != 'None':
                                for h in d['program_id__sector_budget'].split(','):
                                    x = h.split(':')
                                    if int(x[0]) in sub_sector:
                                        sub_sec_budget = float(x[1])
                        if d['allocated_budget']:
                            total_new_budget1 += (d['allocated_budget']
                                                  * sub_sec_budget) / 100

                if request.GET.getlist('sector_id'):
                    if not request.GET.getlist('sub_sector_id'):
                        budget = total_new_budget1
                    else:
                        budget = total_new_budget1
                elif request.GET.getlist('sub_sector_id'):
                    budget = total_new_budget1
                else:
                    all_budget_test = query.values('allocated_budget')
                    s = 0
                    for h in all_budget_test:
                        s += h['allocated_budget']
                    budget = s
                comp = query.values_list(
                    'component_id__name', flat=True).distinct()
                part = query.values_list(
                    'supplier_id__name', flat=True).distinct()
                sect = query.exclude(program_id__sector__name=None).values_list('program_id__sector__name',
                                                                                flat=True).distinct()
                sub_sect = query.exclude(program_id__sub_sector__name=None).values_list(
                    'program_id__sub_sector__name', flat=True).distinct()
                mark = query.values_list(
                    'program_id__marker_category__name', flat=True).distinct()
                mark_value = query.values_list(
                    'program_id__marker_value__value', flat=True).distinct()

            else:
                budget = 0
                prog = []
                comp = []
                part = []
                sect = []
                sub_sect = []
                mark = []
                mark_value = []

            data.append({
                'id': municipality['id'],
                'name': municipality['name'],
                'code': str(municipality['code']),
                'province_name': str(municipality['province_id__name']),
                'district_name': str(municipality['district_id__name']),
                'allocated_budget': budget,
                'program': prog,
                'component': comp,
                'partner': part,
                'sector': sect,
                'sub_sector': sub_sect,
                'marker_category': mark,
                'marker_value': mark_value
            })
        return Response({"results": data})


class SummaryData(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = True
    serializer_class = FivewSerializer

    def list(self, request, *args, **kwargs):
        count = []
        if request.GET.getlist('program_id'):
            prov = request.GET['program_id']
            program = prov.split(",")
            for i in range(0, len(program)):
                program[i] = int(program[i])
        else:
            program = list(Program.objects.values_list('id', flat=True))
            count.append('program')

        if request.GET.getlist('supplier_id'):
            supp = request.GET['supplier_id']
            supplier = supp.split(",")
            for i in range(0, len(supplier)):
                supplier[i] = int(supplier[i])
        else:
            supplier = list(Partner.objects.values_list('id', flat=True))
            count.append('supplier')

        if request.GET.getlist('component_code'):
            comp = request.GET['component_code']
            component = comp.split(",")
            for i in range(0, len(component)):
                component[i] = str(component[i])
        else:
            component = list(Project.objects.values_list('code', flat=True))
            count.append('component')

        if request.GET.getlist('marker_category_id'):
            mc = request.GET['marker_category_id']
            markers = mc.split(",")
            for i in range(0, len(markers)):
                markers[i] = int(markers[i])
        else:
            markers = list(MarkerCategory.objects.values_list('id', flat=True))
            count.append('markers')

        if request.GET.getlist('status'):
            st = request.GET['status']
            stat = st.split(",")
            for i in range(0, len(stat)):
                stat[i] = str(stat[i]).lower()
        else:
            stat = list(FiveW.objects.values_list('status', flat=True))
            count.append('stat')

        if request.GET.getlist('marker_value_id'):
            mv = request.GET['marker_value_id']
            markers_value = mv.split(",")
            for i in range(0, len(markers_value)):
                markers_value[i] = int(markers_value[i])
        else:
            markers_value = list(
                MarkerValues.objects.values_list('id', flat=True))
            count.append('markers_value')

        if request.GET.getlist('sector_id'):
            sect = request.GET['sector_id']
            sector = sect.split(",")
            for i in range(0, len(sector)):
                sector[i] = int(sector[i])
        else:
            sector = list(Sector.objects.values_list('id', flat=True))
            count.append('sector')

        if request.GET.getlist('sub_sector_id'):
            subsect = request.GET['sub_sector_id']
            sub_sector = subsect.split(",")
            for i in range(0, len(sub_sector)):
                sub_sector[i] = int(sub_sector[i])
        else:
            sub_sector = list(SubSector.objects.values_list('id', flat=True))
            count.append('sub_sector')

        if len(count) != 0:
            if len(count) == 8:
                query = FiveW.objects.values(
                    'allocated_budget', 'component_id', 'program_id')
            else:
                query = fivew(supplier, program, component, sector, sub_sector, markers, markers_value,
                              count, stat)
        else:
            query = fivew(supplier, program, component, sector, sub_sector, markers, markers_value,
                          count, stat)

        program = query.distinct('program_id').count()
        total_new_budget1 = 0
        if request.GET.getlist('sector_id'):
            if not request.GET.getlist('sub_sector_id'):
                da = query.values('program_id__id', 'program_id__sector_budget', 'program_id__total_budget',
                                  'allocated_budget')
                sub_sec = [i.id for i in SubSector.objects.filter(
                    sector_id__in=sector)]
                for d in da:
                    sec_budget = 0
                    if d['program_id__sector_budget']:
                        if d['program_id__sector_budget'] != 'None':
                            for h in d['program_id__sector_budget'].split(','):
                                x = h.split(':')
                                if int(x[0]) in sub_sec:
                                    try:
                                        sec_budget += float(x[1])
                                    except:
                                        pass

                    if d['allocated_budget']:
                        print(sec_budget)
                        print(d['allocated_budget'])
                        total_new_budget1 += (d['allocated_budget']
                                              * sec_budget) / 100
            else:
                da = query.values('program_id__id', 'program_id__sector_budget', 'program_id__total_budget',
                                  'allocated_budget')
                for d in da:
                    sub_sec_budget = 0
                    if d['program_id__sector_budget']:
                        if d['program_id__sector_budget'] != 'None':
                            for h in d['program_id__sector_budget'].split(','):
                                x = h.split(':')
                                if int(x[0]) in sub_sector:
                                    sub_sec_budget = float(x[1])
                    if d['allocated_budget']:
                        total_new_budget1 += (d['allocated_budget']
                                              * sub_sec_budget) / 100
        elif request.GET.getlist('sub_sector_id'):
            da = query.values('program_id__id', 'program_id__sector_budget', 'program_id__total_budget',
                              'allocated_budget')
            for d in da:
                sub_sec_budget = 0
                if d['program_id__sector_budget']:
                    if d['program_id__sector_budget'] != 'None':
                        for h in d['program_id__sector_budget'].split(','):
                            x = h.split(':')
                            if int(x[0]) in sub_sector:
                                sub_sec_budget = float(x[1])
                if d['allocated_budget']:
                    total_new_budget1 += (d['allocated_budget']
                                          * sub_sec_budget) / 100

        if request.GET.getlist('sector_id'):
            if not request.GET.getlist('sub_sector_id'):
                all_budget = total_new_budget1
            else:
                all_budget = total_new_budget1
        elif request.GET.getlist('sub_sector_id'):
            all_budget = total_new_budget1
        else:
            if query.aggregate(Sum('allocated_budget')).get('allocated_budget__sum') is None:
                all_budget_test = {'allocated_budget__sum': 0}
                all_budget = all_budget_test['allocated_budget__sum']
            else:
                all_budget_test = query.values('allocated_budget')
                s = 0
                for h in all_budget_test:
                    s += h['allocated_budget']
                all_budget = s
        fivbudget = FiveW.objects.values(
            'allocated_budget', 'program_id', 'component_id', 'supplier_id')
        allocated_sum = all_budget
        component = query.distinct('component_id').count()
        partner = query.distinct('supplier_id').count()
        sector = query.distinct('program_id__sector').count()
        total_program = fivbudget.distinct('program_id').count()
        total_partner = fivbudget.distinct('supplier_id').count()
        total_component = fivbudget.distinct('component_id').count()
        total_sector = Sector.objects.all().count()
        fivbudget = FiveW.objects.values('allocated_budget')
        total_budget = 0
        for b in fivbudget:
            total_budget += b['allocated_budget']

        return Response({
            'allocated_budget': allocated_sum,
            'program': program,
            'partner': partner,
            'component': component,
            'sector': sector,
            'total_allocated_budget': total_budget,
            'total_program': total_program,
            'total_partner': total_partner,
            'total_component': total_component,
            'total_sector': total_sector
        })


class ContractSum(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]

    # filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'supplier_id', 'program_id',
                        'component_id', 'second_tier_partner', ]

    def get_queryset(self):
        queryset = BudgetToSecondTier.objects.order_by('id')

        return queryset

    def get_serializer_class(self):
        serializer_class = ContractSumSerializer
        return serializer_class


class IndicatorApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'category',
                        'indicator', 'is_covid', 'is_dashboard']

    def get_queryset(self):
        queryset = Indicator.objects.exclude(
            show_flag=False, is_dashboard=False).order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = IndicatorSerializer
        return serializer_class


class IndicatorData(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]

    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['id', 'indicator_id', 'district_id']

    def get_queryset(self):
        id_indicators = self.request.GET['indicator_id']
        id_indicator = id_indicators.split(",")
        for i in range(0, len(id_indicator)):
            id_indicator[i] = int(id_indicator[i])

        if self.request.GET.getlist('province_id'):
            province = self.request.GET['province_id']
            province_ids = province.split(",")
            for i in range(0, len(province_ids)):
                province_ids[i] = int(province_ids[i])
            queryset = IndicatorValue.objects.filter(indicator_id__in=id_indicator,
                                                     gapanapa_id__district_id__province_id__id__in=province_ids).select_related(
                'gapanapa_id', 'indicator_id').order_by('id')

        if self.request.GET.getlist('district_id'):
            dist = self.request.GET['district_id']
            district_ids = dist.split(",")
            for i in range(0, len(district_ids)):
                district_ids[i] = int(district_ids[i])
            queryset = IndicatorValue.objects.filter(indicator_id__in=id_indicator,
                                                     gapanapa_id__district_id__id__in=district_ids).select_related(
                'gapanapa_id', 'indicator_id').order_by('id')

        else:

            if self.request.GET.getlist('province_id') == []:
                print('herer')
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
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        group = Group.objects.get(user=user)
        if group.name == 'admin':
            queryset = Notification.objects.order_by('-id')
        else:
            queryset = Notification.objects.filter(user=user).order_by('-id')
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
    filterset_fields = ['id', 'name', 'program_id',
                        'sector', 'sub_sector', 'code', 'partner_id']

    def get_queryset(self):
        queryset = Project.objects.order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = ProjectSerializer
        return serializer_class


class ProgramTestApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'marker_value', 'marker_category']

    def get_queryset(self):
        if self.request.GET.getlist('program'):
            prov = self.request.GET['program']
            program_filter_id = prov.split(",")
            for i in range(0, len(program_filter_id)):
                program_filter_id[i] = int(program_filter_id[i])
            queryset = Program.objects.filter(
                id__in=program_filter_id).order_by('id')
        elif self.request.GET.getlist('component_code'):
            comp = self.request.GET['component_code']
            component_filter_code = comp.split(",")
            ids = []
            for i in range(0, len(component_filter_code)):
                test = Project.objects.get(code=str(component_filter_code[i]))
                ids.append(test.program_id.id)
            queryset = Program.objects.filter(id__in=ids).order_by('id')
        elif self.request.GET.getlist('start_date') and self.request.GET.getlist('end_date'):
            start_date = self.request.GET['start_date']
            end_date = self.request.GET['end_date']
            program = Program.objects.values('start_date', 'end_date', 'id')
            ids = []
            for p in program:
                if p['start_date'] and p['end_date'] is not None:
                    a = start_date.split('-')
                    start_date_new = date(int(a[0]), int(a[1]), int(a[2]))
                    b = end_date.split('-')
                    end_date_new = date(int(b[0]), int(b[1]), int(b[2]))
                    print(str('Start Date') + ':' + str(start_date) +
                          str('End Date') + ':' + str(end_date))
                    user_timerange = DateTimeRange(
                        end_date_new, start_date_new)
                    program_timerange = DateTimeRange(
                        p['start_date'], p['end_date'])

                    if user_timerange in program_timerange:
                        ids.append(p['id'])
            queryset = Program.objects.filter(id__in=ids).order_by('id')
        else:
            queryset = Program.objects.order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = ProgramSerializer
        return serializer_class


class TravelTimeApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    # authentication_classes = (TokenAuthentication, BasicAuthentication)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'gapanapa', 'facility_type',
                        'travel_category_population', 'season', 'travel_category']

    def get_queryset(self):
        queryset = TravelTime.objects.select_related('gapanapa').order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = TravelTimeSerializer
        return serializer_class


class CovidChoice(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = True
    serializer_class = FivewSerializer

    def list(self, request, *args, **kwargs):
        return Response({
            'field': [{'name': 'Kathmandu Activity', 'value': 'kathmandu_activity'},
                      {'name': 'Providing TA to Local government',
                          'value': 'providing_ta_to_local_government'},
                      {'name': 'Providing TA To Provincial Government',
                       'value': 'providing_ta_to_provincial_government'}],
            'kathmandu_activity': ['Intervention', 'Influence', 'N/A'],
            'other': ['NA - Complete', 'Yes', 'Partial High', 'Partial Low', 'No']
        })


class Popup(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = FiveW.objects.all()
    serializer_class = FivewSerializer

    def list(self, request, *args, **kwargs):
        program_data = []
        count = []
        if request.GET.getlist('program_id'):
            prov = request.GET['program_id']
            program = prov.split(",")
            for i in range(0, len(program)):
                program[i] = int(program[i])
        else:
            program = list(Program.objects.values_list('id', flat=True))
            count.append('program')

        if request.GET.getlist('supplier_id'):
            supp = request.GET['supplier_id']
            supplier = supp.split(",")
            for i in range(0, len(supplier)):
                supplier[i] = int(supplier[i])
        else:
            supplier = list(Partner.objects.values_list('id', flat=True))
            count.append('supplier')

        if request.GET.getlist('component_code'):
            comp = request.GET['component_code']
            component = comp.split(",")
            for i in range(0, len(component)):
                component[i] = str(component[i])
        else:
            component = list(Project.objects.values_list('code', flat=True))
            count.append('component')

        if request.GET.getlist('status'):
            st = request.GET['status']
            stat = st.split(",")
            for i in range(0, len(stat)):
                stat[i] = str(stat[i]).lower()
        else:
            stat = list(FiveW.objects.values_list('status', flat=True))
            count.append('stat')

        if request.GET.getlist('marker_category_id'):
            mc = request.GET['marker_category_id']
            markers = mc.split(",")
            for i in range(0, len(markers)):
                markers[i] = int(markers[i])
        else:
            markers = list(MarkerCategory.objects.values_list('id', flat=True))
            count.append('markers')

        if request.GET.getlist('marker_value_id'):
            mv = request.GET['marker_value_id']
            markers_value = mv.split(",")
            for i in range(0, len(markers_value)):
                markers_value[i] = int(markers_value[i])
        else:
            markers_value = list(
                MarkerValues.objects.values_list('id', flat=True))
            count.append('markers_value')

        if request.GET.getlist('sector_id'):
            sect = request.GET['sector_id']
            sector = sect.split(",")
            for i in range(0, len(sector)):
                sector[i] = int(sector[i])
        else:
            sector = list(Sector.objects.values_list('id', flat=True))
            count.append('sector')

        if request.GET.getlist('sub_sector_id'):
            subsect = request.GET['sub_sector_id']
            sub_sector = subsect.split(",")
            for i in range(0, len(sub_sector)):
                sub_sector[i] = int(sub_sector[i])
        else:
            sub_sector = list(SubSector.objects.values_list('id', flat=True))
            count.append('sub_sector')

        if count:
            if len(count) == 8:
                query = FiveW.objects.values(
                    'allocated_budget', 'component_id', 'program_id')
            else:
                query = fivew(supplier, program, component, sector, sub_sector, markers, markers_value,
                              count, stat)
        else:
            query = fivew(supplier, program, component, sector, sub_sector, markers, markers_value,
                          count, stat)

        if request.GET.getlist('field'):
            field = request.GET['field']
            value = request.GET['value']
            kwargs = {
                '{0}__iexact'.format(field): value
            }
            query = query.filter(Q(**kwargs))
        total_final_budget = 0
        if query.exists():
            program = query.values('program_id', 'program_id__name').annotate(
                Sum('allocated_budget'))
            total_final_budget = 0
            for p in program:
                pid = Program.objects.get(id=p['program_id'])
                if request.GET.getlist('sector_id') or request.GET.getlist('sub_sector_id'):
                    sec_id_list = [i['id']
                                   for i in pid.sector.all().values('id')]
                    pt = len(list(set(sec_id_list).intersection(sector)))
                    sub_sec_id_list = [i['id']
                                       for i in pid.sub_sector.all().values('id')]
                    dt = len(list(set(sub_sec_id_list).intersection(sub_sector)))
                sec_budget = 0
                if request.GET.getlist('sector_id'):
                    if not request.GET.getlist('sub_sector_id'):
                        sub_sect = [i.id for i in
                                    SubSector.objects.filter(sector_id__in=sector)]
                        if pid.sector_budget is not None:
                            for h in pid.sector_budget.split(','):
                                x = h.split(':')
                                if int(x[0]) in sub_sect:
                                    try:
                                        sec_budget += float(x[1])
                                    except:
                                        pass
                    else:
                        if pid.sector_budget is not None:
                            for h in pid.sector_budget.split(','):
                                x = h.split(':')
                                # print(str(int(x[0])) + ":" + str((x[1])))
                                if int(x[0]) in sub_sector:
                                    try:
                                        sec_budget += float(x[1])
                                    except:
                                        pass
                elif request.GET.getlist('sub_sector_id'):
                    if pid.sector_budget is not None:
                        for j in pid.sector_budget.split(','):
                            y = j.split(':')
                            if int(y[0]) in sub_sector:
                                try:
                                    sec_budget += float(y[1])
                                except:
                                    pass
                marker_data = []
                program_sector = []
                component_data = []
                p_data = Program.objects.get(id=p['program_id'])
                for marker in p_data.marker_value.all():
                    marker_data.append({
                        'marker_category': marker.marker_category_id.name,
                        'marker_value': marker.value
                    })
                for sectors in p_data.sub_sector.all():
                    program_sector.append({
                        'id': sectors.id,
                        'sector': sectors.sector_id.name,
                        'sub_sector': sectors.name,
                    })
                c_data = query.values('component_id', 'component_id__name').filter(program_id=p['program_id']).annotate(
                    Sum('allocated_budget'))

                for c in c_data:
                    sector_data = []
                    partner_data = []
                    s_data = Project.objects.get(id=c['component_id'])
                    part_data = query.values('supplier_id', 'supplier_id__name').filter(
                        program_id=p['program_id'], component_id=c['component_id']).annotate(
                        Sum('allocated_budget'))
                    for part in part_data:
                        partner_data.append({
                            'id': part['supplier_id'],
                            'name': part['supplier_id__name'],
                            'partner_budget': part['allocated_budget__sum'],
                        })
                    for sectors in s_data.sub_sector.all():
                        sector_data.append({
                            'id': sectors.id,
                            'sector': sectors.sector_id.name,
                            'sub_sector': sectors.name,
                        })
                    component_data.append({
                        'id': c['component_id'],
                        'name': c['component_id__name'],
                        'component_budget': c['allocated_budget__sum'],
                        'sectors': sector_data,
                        'partners': partner_data,
                    })
                if request.GET.getlist('sector_id'):
                    program_budget = (
                        (p['allocated_budget__sum'] * sec_budget) / 100) / pt
                elif request.GET.getlist('sub_sector_id'):
                    program_budget = (
                        (p['allocated_budget__sum'] * sec_budget) / 100) / dt
                else:
                    program_budget = p['allocated_budget__sum']
                total_final_budget += program_budget
                program_data.append({
                    'id': p['program_id'],
                    'program': p['program_id__name'],
                    'sector': program_sector,
                    'program_budget': program_budget,
                    'markers': marker_data,
                    'components': component_data,
                })
        total_budget = total_final_budget
        return Response({"total_budget": total_budget, "programs": program_data})


class Feedback(viewsets.ViewSet):
    queryset = FeedbackForm.objects.all()
    serializer_class = FeedbackSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegionalSectorGraph(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = FiveW.objects.all()
    serializer_class = FivewSerializer

    def list(self, request, *args, **kwargs):
        if request.GET['region'] == 'province':
            sector_ids = []
            sector_by_buget = []
            top_sector_by_no_partner = []
            if 'province_code' in request.GET:
                five = FiveW.objects.filter(province_id__code=int(request.GET['province_code'])).values(
                    'id',
                    'program_id__sector__id',
                ).distinct()
                for f in five:
                    sector_ids.append(f['program_id__sector__id'])

                def unique(list1):
                    unique_list = []
                    finaldata = []
                    for x in list1:
                        if x not in unique_list:
                            unique_list.append(x)
                    for x in unique_list:
                        finaldata.append(x)
                    if None in finaldata:
                        finaldata.remove(None)
                    return finaldata

                sectoruniqueid = unique(sector_ids)
                if len(sectoruniqueid) != 0:
                    for s in sectoruniqueid:
                        sector_sub_sector_new = []
                        sub_sector_final_data = []
                        dat = FiveW.objects.filter(program_id__sector=s,
                                                   province_id__code=int(request.GET['province_code'])).exclude(
                            allocated_budget=None)
                        sector = Sector.objects.get(id=s)
                        set = SubSector.objects.filter(
                            sector_id=sector.id).values('name')
                        for v in set:
                            sector_sub_sector_new.append(v['name'])
                        sub_sec = [i['id'] for i in SubSector.objects.filter(
                            sector_id=sector.id).values('id')]
                        total_budgetnew = 0
                        partner_name = []
                        for d in dat:
                            sub_sectors = []
                            sub_sector_final = []
                            sub_sectors.append(
                                list(d.program_id.sub_sector.values_list('name', flat=True)))
                            for s in sub_sectors:
                                for di in s:
                                    sub_sector_final.append(di)
                            ho = d.program_id.sector_budget
                            sec_budget = 0
                            if ho:
                                if ho != 'None':
                                    for h in ho.split(','):
                                        x = h.split(':')
                                        if int(x[0]) in sub_sec:
                                            try:
                                                sec_budget += float(x[1])
                                            except:
                                                pass
                            if d.allocated_budget:
                                total_budgetnew += (d.allocated_budget *
                                                    sec_budget) / 100
                            partner_count = d.program_id.partner_id.all().values('name')
                            for p in partner_count:
                                if p['name'] not in partner_name:
                                    partner_name.append(p['name'])
                        if dat:
                            last_sub_sector = unique(sub_sector_final)
                        else:
                            sub_sector_final = []
                            last_sub_sector = unique(sub_sector_final)
                        for l in last_sub_sector:
                            if l in sector_sub_sector_new:
                                sub_sector_final_data.append(l)
                        sector_by_buget.append({
                            'id': sector.id,
                            'name': sector.name,
                            'sub_sector': sub_sector_final_data,
                            'key': 'total_budget',
                            'value': total_budgetnew

                        })
                        top_sector_by_no_partner.append({

                            'id': sector.id,
                            'name': sector.name,
                            'key': 'partner_count',
                            'value': len(partner_name)
                        })
                test1 = sorted(sector_by_buget,
                               key=lambda i: i['value'], reverse=True)
                test4 = sorted(top_sector_by_no_partner,
                               key=lambda i: i['value'], reverse=True)
                return Response({'active_sectors': test1, 'top_sector_by_no_of_partner': test4})
            else:
                return Response({"results": "Please Pass Province Code"})

        elif request.GET['region'] == 'district':
            sector_ids = []
            sector_by_buget = []
            top_sector_by_no_partner = []
            if 'district_code' in request.GET:
                five = FiveW.objects.filter(district_id__code=int(request.GET['district_code'])).values(
                    'id',
                    'program_id__sector__id',
                ).distinct()
                for f in five:
                    sector_ids.append(f['program_id__sector__id'])

                def unique(list1):
                    unique_list = []
                    finaldata = []
                    for x in list1:
                        if x not in unique_list:
                            unique_list.append(x)
                    for x in unique_list:
                        finaldata.append(x)
                    if None in finaldata:
                        finaldata.remove(None)
                    return finaldata

                sectoruniqueid = unique(sector_ids)
                if len(sectoruniqueid) != 0:
                    for s in sectoruniqueid:
                        sector_sub_sector_new = []
                        sub_sector_final_data = []
                        dat = FiveW.objects.filter(program_id__sector=s,
                                                   district_id__code=int(request.GET['district_code'])).exclude(
                            allocated_budget=None)
                        sector = Sector.objects.get(id=s)
                        set = SubSector.objects.filter(
                            sector_id=sector.id).values('name')
                        for v in set:
                            sector_sub_sector_new.append(v['name'])
                        sub_sec = [i['id'] for i in SubSector.objects.filter(
                            sector_id=sector.id).values('id')]
                        total_budgetnew = 0
                        partner_name = []
                        for d in dat:
                            sub_sectors = []
                            sub_sector_final = []
                            sub_sectors.append(
                                list(d.program_id.sub_sector.values_list('name', flat=True)))
                            for s in sub_sectors:
                                for di in s:
                                    sub_sector_final.append(di)
                            ho = d.program_id.sector_budget
                            sec_budget = 0
                            if ho:
                                if ho != 'None':
                                    for h in ho.split(','):
                                        x = h.split(':')
                                        if int(x[0]) in sub_sec:
                                            try:
                                                sec_budget += float(x[1])
                                            except:
                                                pass
                            if d.allocated_budget:
                                total_budgetnew += (d.allocated_budget *
                                                    sec_budget) / 100
                            partner_count = d.program_id.partner_id.all().values('name')
                            for p in partner_count:
                                if p['name'] not in partner_name:
                                    partner_name.append(p['name'])
                        if dat:
                            last_sub_sector = unique(sub_sector_final)
                        else:
                            sub_sector_final = []
                            last_sub_sector = unique(sub_sector_final)
                        for l in last_sub_sector:
                            if l in sector_sub_sector_new:
                                sub_sector_final_data.append(l)
                        sector_by_buget.append({
                            'id': sector.id,
                            'name': sector.name,
                            'sub_sector': sub_sector_final_data,
                            'key': 'total_budget',
                            'value': total_budgetnew

                        })
                        top_sector_by_no_partner.append({

                            'id': sector.id,
                            'name': sector.name,
                            'key': 'partner_count',
                            'value': len(partner_name)
                        })
                test1 = sorted(sector_by_buget,
                               key=lambda i: i['value'], reverse=True)
                test4 = sorted(top_sector_by_no_partner,
                               key=lambda i: i['value'], reverse=True)
                return Response({'active_sectors': test1, 'top_sector_by_no_of_partner': test4})
            else:
                return Response({"results": "Please Pass District Code"})
        elif request.GET['region'] == 'municipality':
            sector_ids = []
            sector_by_buget = []
            top_sector_by_no_partner = []
            if 'municipality_code' in request.GET:
                five = FiveW.objects.filter(municipality_id__code=int(request.GET['municipality_code'])).values(
                    'id',
                    'program_id__sector__id').distinct()

                for f in five:
                    sector_ids.append(f['program_id__sector__id'])

                def unique(list1):
                    unique_list = []
                    finaldata = []
                    for x in list1:
                        if x not in unique_list:
                            unique_list.append(x)
                    for x in unique_list:
                        finaldata.append(x)
                    if None in finaldata:
                        finaldata.remove(None)
                    return finaldata

                sectoruniqueid = unique(sector_ids)
                if len(sectoruniqueid) != 0:
                    for s in sectoruniqueid:
                        sector_sub_sector_new = []
                        sub_sector_final_data = []
                        dat = FiveW.objects.filter(program_id__sector=s,
                                                   municipality_id__code=int(request.GET['municipality_code'])).exclude(
                            allocated_budget=None)
                        sector = Sector.objects.get(id=s)
                        set = SubSector.objects.filter(
                            sector_id=sector.id).values('name')
                        for v in set:
                            sector_sub_sector_new.append(v['name'])
                        sub_sec = [i['id'] for i in SubSector.objects.filter(
                            sector_id=sector.id).values('id')]
                        total_budgetnew = 0
                        partner_name = []
                        for d in dat:
                            sub_sectors = []
                            sub_sector_final = []
                            sub_sectors.append(
                                list(d.program_id.sub_sector.values_list('name', flat=True)))
                            for s in sub_sectors:
                                for di in s:
                                    sub_sector_final.append(di)
                            ho = d.program_id.sector_budget
                            sec_budget = 0
                            if ho:
                                if ho != 'None':
                                    for h in ho.split(','):
                                        x = h.split(':')
                                        if int(x[0]) in sub_sec:
                                            try:
                                                sec_budget += float(x[1])
                                            except:
                                                pass
                            if d.allocated_budget:
                                total_budgetnew += (d.allocated_budget *
                                                    sec_budget) / 100
                            partner_count = d.program_id.partner_id.all().values('name')
                            for p in partner_count:
                                if p['name'] not in partner_name:
                                    partner_name.append(p['name'])
                        if dat:
                            last_sub_sector = unique(sub_sector_final)
                        else:
                            sub_sector_final = []
                            last_sub_sector = unique(sub_sector_final)
                        for l in last_sub_sector:
                            if l in sector_sub_sector_new:
                                sub_sector_final_data.append(l)
                        sector_by_buget.append({
                            'id': sector.id,
                            'name': sector.name,
                            'sub_sector': sub_sector_final_data,
                            'key': 'total_budget',
                            'value': total_budgetnew

                        })
                        top_sector_by_no_partner.append({

                            'id': sector.id,
                            'name': sector.name,
                            'key': 'partner_count',
                            'value': len(partner_name)
                        })

                test1 = sorted(sector_by_buget,
                               key=lambda i: i['value'], reverse=True)
                test4 = sorted(top_sector_by_no_partner,
                               key=lambda i: i['value'], reverse=True)
                return Response({'active_sectors': test1, 'top_sector_by_no_of_partner': test4})
            else:
                return Response({"results": "Please Pass Municipality Code"})
        else:
            return Response({"results": "Invalid Region"})
