from rest_framework import serializers
from .models import Partner, Program, MarkerValues, MarkerCategory, District, Province, GapaNapa, FiveW, Indicator, \
    IndicatorValue, Sector, SubSector, TravelTime, GisLayer, Project, Output, Notification, BudgetToSecondTier, \
    Filter, NepalSummary, FeedbackForm, FAQ, TermsAndCondition, NationalStatistic,Manual


class NepalSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = NepalSummary
        fields = '__all__'


class NetionalStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = NationalStatistic
        fields = '__all__'


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'


class TermsAndConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsAndCondition
        fields = '__all__'


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = '__all__'


class MarkerCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkerCategory
        fields = '__all__'


class GisLayerSerializer(serializers.ModelSerializer):
    style = serializers.SerializerMethodField()
    popup_info = serializers.SerializerMethodField()

    class Meta:
        model = GisLayer
        fields = ('id', 'name', 'layer_name', 'workspace', 'geoserver_url', 'store_name', 'type',
                  'geo_type', 'identifier_key', 'filename', 'description', 'style', 'popup_info')

    def get_style(self, instance):
        styl = []
        styles = instance.GisStyle.all()
        for style in styles:
            styl.append({
                'id': style.id,
                'circle_color': style.circle_color,
                'fill_color': style.fill_color,
                'circle_radius': style.circle_radius,
                'layer': style.layer.id
            })
        return styl

    def get_popup_info(self, instance):
        pop = []
        pops = instance.GisPop.all()
        for p in pops:
            pop.append({
                'id': p.id,
                'key': p.key,
                'title': p.title,
                'type': p.type,
                'layer': p.layer.id
            })
        return pop


class OutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Output
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class MarkerValuesSerializer(serializers.ModelSerializer):
    marker_category = serializers.SerializerMethodField()

    class Meta:
        model = MarkerValues
        fields = ('id', 'value', 'marker_category_id', 'marker_category')

    def get_marker_category(self, obj):
        return str(obj.marker_category_id.name)


class ProgramSerializer(serializers.ModelSerializer):
    marker_value = serializers.SerializerMethodField()
    marker_category = serializers.SerializerMethodField()
    sector = serializers.SerializerMethodField()
    sub_sector = serializers.SerializerMethodField()
    component = serializers.SerializerMethodField()
    partner = serializers.SerializerMethodField()

    class Meta:
        model = Program
        fields = (
            'id', 'name', 'start_date', 'end_date', 'code', 'iati', 'total_budget', 'partner', 'component',
            'marker_category', 'marker_value',
            'sector',
            'sub_sector')

    def get_partner(self, obj):
        data = []
        qs = obj.partner_id.all().values('name', 'id')
        for q in qs:
            data.append({
                'id': q['id'],
                'name': q['name']

            })
        return data

    def get_component(self, obj):
        data = []
        qs = obj.ProjectProgram.values('id', 'name', 'code').distinct('code')
        for q in qs:
            data.append({
                'id': q['id'],
                'code': q['code'],
                'name': q['name']

            })

        return data

    def get_marker_category(self, obj):
        data = []
        qs = obj.marker_value.all().values('marker_category_id', 'marker_category_id__name')
        for q in qs:
            data.append({
                'id': q['marker_category_id'],
                'name': q['marker_category_id__name']

            })
        return data

    def get_marker_value(self, obj):
        data = []
        qs = obj.marker_value.all().values('id', 'value', 'marker_category_id__name')
        for q in qs:
            data.append({
                'id': q['id'],
                'name': q['value'],
                # 'cat': q['marker_category_id__name']

            })
        return data

    def get_sector(self, obj):
        data = []
        qs = obj.sector.all().values('id', 'name').distinct('name')

        for q in qs:
            data.append({
                'id': q['id'],
                'name': q['name']

            })

        return data

    def get_sub_sector(self, obj):
        data = []
        qs = obj.sub_sector.values('id', 'name').distinct('name')

        for q in qs:
            data.append({
                'id': q['id'],
                'name': q['name']

            })

        return data


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ('id', 'name', 'code', 'bbox')


class FilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filter

        fields = ('name', 'options',)


class IndicatorSerializer(serializers.ModelSerializer):
    filter = FilterSerializer(many=True, read_only=True)

    class Meta:
        model = Indicator
        fields = (
            'id', 'full_title', 'abstract', 'category', 'source', 'federal_level', 'is_covid', 'is_dashboard', 'filter',
            'unit',
            'data_type', 'url')


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = '__all__'

class ManualSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manual
        fields = '__all__'


class SubsectorSerializer(serializers.ModelSerializer):
    sector_name = serializers.SerializerMethodField()

    class Meta:
        model = SubSector
        fields = ('id', 'sector_id', 'sector_name', 'name', 'code')

    def get_sector_name(self, obj):
        return str(obj.sector_id.name)


class ProjectSerializer(serializers.ModelSerializer):
    sub_sector = serializers.SerializerMethodField()
    sector = serializers.SerializerMethodField()
    partners = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'name', 'sector', 'sub_sector', 'code', 'partners')

    def get_sub_sector(self, obj):
        qs = obj.sub_sector.all().order_by('id').values_list('id', flat=True)
        return qs

    def get_sector(self, obj):
        qs = obj.sector.all().order_by('id').values_list('id', flat=True)
        # qs = obj.sub_sector.all().order_by('id').values('sub_sector_name', 'sub_sector_code')
        return qs

    def get_partners(self, obj):
        qs = obj.partner_id.all().order_by('id').values_list('id', flat=True)
        return qs


class ContractSumSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetToSecondTier
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    province_name = serializers.SerializerMethodField()

    class Meta:
        model = District
        fields = ('id', 'province_id', 'province_name', 'name', 'code', 'n_code', 'bbox')

    def get_province_name(self, obj):
        return str(obj.province_id.name)


class GaanapaSerializer(serializers.ModelSerializer):
    code = serializers.SerializerMethodField()
    province_name = serializers.SerializerMethodField()
    district_name = serializers.SerializerMethodField()

    class Meta:
        model = GapaNapa
        fields = (
            'id', 'province_id', 'district_id', 'province_name', 'district_name', 'hlcit_code', 'name', 'gn_type_np',
            'code', 'population', 'bbox')

    def get_code(self, obj):
        return str(obj.code)

    def get_district_name(self, obj):
        return obj.district_id.name

    def get_province_name(self, obj):
        return str(obj.province_id.name)


class FivewSerializer(serializers.ModelSerializer):
    # partner_name = serializers.SerializerMethodField()
    # program_name = serializers.SerializerMethodField()
    # province = serializers.SerializerMethodField()
    # district = serializers.SerializerMethodField()
    # gapa_napa = serializers.SerializerMethodField()
    # implenting_partner_first = serializers.SerializerMethodField()
    # implenting_partner_second = serializers.SerializerMethodField()
    # implenting_partner_third = serializers.SerializerMethodField()

    class Meta:
        model = FiveW
        fields = '__all__'
    #     fields = (
    #         'id', 'partner_name', 'program_name', 'province', 'district', 'gapa_napa', 'status', 'start_date',
    #         'end_date',
    #         'reporting_ministry_line', 'implenting_partner_first', 'implenting_partner_second',
    #         'implenting_partner_third')

    # def get_partner_name(self, obj):
    #     return str(obj.partner_name)
    #
    # def get_program_name(self, obj):
    #     return str(obj.program_name)
    #
    # def get_province(self, obj):
    #     return str(obj.province)
    #
    # def get_district(self, obj):
    #     return str(obj.district)
    #
    # def get_gapa_napa(self, obj):
    #     return str(obj.gapa_napa.name)
    #
    # def get_implenting_partner_first(self, obj):
    #     return str(obj.implenting_partner_first)
    #
    # def get_implenting_partner_second(self, obj):
    #     return str(obj.implenting_partner_second)
    #
    # def get_implenting_partner_third(self, obj):
    #     return str(obj.implenting_partner_third)


class IndicatorValueSerializer(serializers.ModelSerializer):
    code = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    # indicator_name = serializers.SerializerMethodField()

    class Meta:
        model = IndicatorValue
        fields = ('id', 'indicator_id', 'code', 'value','name')

    def get_code(self, obj):
        try:
            return str(obj.gapanapa_id.code)
        except:
            return None

    def get_name(self, obj):
        try:
            return str(obj.gapanapa_id.name)
        except:
            return None

    # def get_indicator_name(self, obj):
    #     return str(obj.indicator_id.indicator)


class TravelTimeSerializer(serializers.ModelSerializer):
    gapanapa = serializers.SerializerMethodField()
    geography = serializers.SerializerMethodField()

    class Meta:
        model = TravelTime
        fields = ('id', 'gapanapa', 'facility_type', 'travel_category_population', 'tc_pc_pop', 'season', 'geography',
                  'travel_category')

    def get_gapanapa(self, obj):
        return str(obj.gapanapa)

    def get_geography(self, obj):
        return str(obj.gapanapa.geography)


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackForm
        fields = ['name', 'email', 'attachment', 'subject', 'your_feedback', 'type']
