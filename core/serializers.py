from rest_framework import serializers
from .models import Partner, Program, MarkerValues, MarkerCategory, District, Province, GapaNapa, FiveW, Indicator, \
    IndicatorValue, Sector, SubSector


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = '__all__'


class MarkerCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkerCategory
        fields = '__all__'


class MarkerValuesSerializer(serializers.ModelSerializer):
    marker_category = serializers.SerializerMethodField()

    class Meta:
        model = MarkerValues
        fields = ('id', 'marker_values', 'marker_category')

    def get_marker_category(self, obj):
        return str(obj.marker_category)


class ProgramSerializer(serializers.ModelSerializer):
    marker = serializers.SerializerMethodField()
    sub_sector = serializers.SerializerMethodField()

    class Meta:
        model = Program
        fields = ('id', 'program_name', 'program_description', 'sub_sector', 'marker')

    def get_marker(self, obj):
        qs = obj.marker.all().order_by('id')
        return MarkerValuesSerializer(qs, many=True, read_only=True).data

    def get_sub_sector(self, obj):
        qs = obj.sub_sector.all().order_by('id')
        return SubsectorSerializer(qs, many=True, read_only=True).data


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'


class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        fields = '__all__'


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = '__all__'


class SubsectorSerializer(serializers.ModelSerializer):
    sector = serializers.SerializerMethodField()

    class Meta:
        model = SubSector
        fields = ('id', 'sector', 'sub_sector_name', 'sub_sector_code')

    def get_sector(self, obj):
        return str(obj.sector)

class DistrictSerializer(serializers.ModelSerializer):
    province = serializers.SerializerMethodField()

    class Meta:
        model = District
        fields = ('id', 'province', 'district_name', 'district_code')

    def get_province(self, obj):
        return str(obj.province)


class GaanapaSerializer(serializers.ModelSerializer):
    province = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()

    class Meta:
        model = GapaNapa
        fields = ('id', 'province', 'district', 'name', 'gn_type_en', 'gn_type_np', 'cbs_code', 'hlcit_code', 'p_code')

    def get_province(self, obj):
        return str(obj.province)

    def get_district(self, obj):
        return str(obj.district)


class FivewSerializer(serializers.ModelSerializer):
    partner_name = serializers.SerializerMethodField()
    program_name = serializers.SerializerMethodField()
    province = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()
    gapa_napa = serializers.SerializerMethodField()
    implenting_partner_first = serializers.SerializerMethodField()
    implenting_partner_second = serializers.SerializerMethodField()
    implenting_partner_third = serializers.SerializerMethodField()

    class Meta:
        model = FiveW
        fields = (
            'id', 'partner_name', 'program_name', 'province', 'district', 'gapa_napa', 'status', 'start_date',
            'end_date',
            'reporting_ministry_line', 'implenting_partner_first', 'implenting_partner_second',
            'implenting_partner_third')

    def get_partner_name(self, obj):
        return str(obj.partner_name)

    def get_program_name(self, obj):
        return str(obj.program_name)

    def get_province(self, obj):
        return str(obj.province)

    def get_district(self, obj):
        return str(obj.district)

    def get_gapa_napa(self, obj):
        return str(obj.gapa_napa.name)

    def get_implenting_partner_first(self, obj):
        return str(obj.implenting_partner_first)

    def get_implenting_partner_second(self, obj):
        return str(obj.implenting_partner_second)

    def get_implenting_partner_third(self, obj):
        return str(obj.implenting_partner_third)


class IndicatorValueSerializer(serializers.ModelSerializer):
    indicator = serializers.SerializerMethodField()
    gapanapa = serializers.SerializerMethodField()
    gapanapa_code = serializers.SerializerMethodField()

    class Meta:
        model = IndicatorValue
        fields = ('id', 'indicator', 'gapanapa', 'gapanapa_code', 'value')

    def get_gapanapa(self, obj):
        return str(obj.gapanapa.name)

    def get_indicator(self, obj):
        return str(obj.indicator.indicator)

    def get_gapanapa_code(self, obj):
        return str(obj.gapanapa.hlcit_code)
