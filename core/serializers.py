from rest_framework import serializers
from .models import Partner, Program, MarkerValues, MarkerCategory, District, Province, GapaNapa, FiveW, Indicator, \
    IndicatorValue, Sector, SubSector, TravelTime, GisLayer, Project, Output, Notification, BudgetToSecondTier, \
    Filter


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

    class Meta:
        model = GisLayer
        fields = ('id', 'name', 'layer_name', 'workspace', 'geoserver_url', 'store_name', 'type',
                  'category', 'filename', 'description', 'style')

    def get_style(self, instance):
        styl = []
        styles = instance.GisStyle.all()
        for style in styles:
            styl.append({
                'id': style.id,
                'color': style.style,
                'fillColor': style.field_color,
                'opacity': style.opacity,
                'fill_opacity': style.field_opacity,
                'layer': style.layer.id
            })
        return styl


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
    sub_sector = serializers.SerializerMethodField()
    sector = serializers.SerializerMethodField()

    class Meta:
        model = Program
        fields = ('id', 'name', 'description', 'sector', 'sub_sector', 'marker_category', 'marker_value', 'partner',
                  'code', 'budget')

    def get_marker_category(self, obj):
        qs = obj.marker_category.order_by('id').values_list('id', flat=True)
        return qs

    def get_marker_value(self, obj):
        qs = obj.marker_value.all().order_by('id').values_list('id', flat=True)
        return qs

    def get_sub_sector(self, obj):
        qs = obj.sub_sector.all().order_by('id').values_list('id', flat=True)
        return qs

    def get_sector(self, obj):
        qs = obj.sector.all().order_by('id').values_list('id', flat=True)
        # qs = obj.sub_sector.all().order_by('id').values('sub_sector_name', 'sub_sector_code')
        return qs


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ('id', 'name', 'code')


class FilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filter
        fields = ('filter', 'options',)


class IndicatorSerializer(serializers.ModelSerializer):
    filter = FilterSerializer(many=True, read_only=True)

    class Meta:
        model = Indicator
        fields = ('id', 'full_title', 'abstract', 'category', 'source', 'federal_level', 'is_covid', 'filter',)


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = '__all__'


class SubsectorSerializer(serializers.ModelSerializer):
    sector_name = serializers.SerializerMethodField()

    class Meta:
        model = SubSector
        fields = ('id', 'sector_id', 'sector_name', 'name', 'code')

    def get_sector_name(self, obj):
        return str(obj.sector_id.name)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class ContractSumSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetToSecondTier
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    # province_name = serializers.SerializerMethodField()

    class Meta:
        model = District
        fields = ('id', 'province_id',  'name', 'code', 'n_code')

    # def get_province_name(self, obj):
    #     return str(obj.province_id.name)


class GaanapaSerializer(serializers.ModelSerializer):
    class Meta:
        model = GapaNapa
        fields = ('id', 'province_id', 'district_id', 'hlcit_code', 'name', 'gn_type_np',
                  'code', 'population')


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

    # indicator_name = serializers.SerializerMethodField()

    class Meta:
        model = IndicatorValue
        fields = ('id', 'indicator_id', 'code', 'value')

    def get_code(self, obj):
        return int(obj.gapanapa_id.code)

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
