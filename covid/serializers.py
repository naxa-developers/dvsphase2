from rest_framework import serializers
from .models import CovidFivew, DryDshosp4hrSums, DryDshosp4hrUncoveredAdm1Sums, DryDshosp8hrSums, \
    DryDshosp8hrUncoveredAdm1Sums, DryDshosp12hrSums, DryDshosp12hrUncoveredAdm1Sums, DryAllCovidsDhfs4hrSums, \
    DryAllCovidsDhfs4hrUncoveredAdm1Sums, DryAllCovidsDhfs8hrSums, DryAllCovidsDhfs8hrUncoveredAdm1Sums, \
    DryAllCovidsDhfs12hrSums, DryAllCovidsDhfs12hrUncoveredAdm1Sums, CovidSpecificProgram, CovidSpecificProgramBudget


class CovidFivewSerializer(serializers.ModelSerializer):
    province_code = serializers.SerializerMethodField()
    district_code = serializers.SerializerMethodField()
    municipality_code = serializers.SerializerMethodField()

    class Meta:
        model = CovidFivew
        fields = (
            'id', 'province_code', 'district_code', 'municipality_code', 'partner', 'program', 'project_name', 'sector')

    def get_province_code(self, obj):
        return str(obj.province_id.code)

    def get_district_code(self, obj):
        return str(obj.district_id.code)

    def get_municipality_code(self, obj):
        return str(obj.municipality_id.code)


class DryDshosp4hrSumsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DryDshosp4hrSums
        fields = '__all__'


class CovidSpecificSerializer(serializers.ModelSerializer):
    province_code = serializers.SerializerMethodField()
    district_code = serializers.SerializerMethodField()
    municipality_code = serializers.SerializerMethodField()
    budget = serializers.SerializerMethodField()

    class Meta:
        model = CovidSpecificProgram
        fields = ('id', 'province_code', 'district_code', 'municipality_code', 'component', 'second_tier_partner',
                  'project_status', 'sector', 'budget', 'kathmandu_activity', 'delivery_in_lockdown',
                  'covid_priority_3_12_Months', 'covid_recovery_priority', 'providing_ta_to_local_government')

    def get_province_code(self, obj):
        if obj.province_id:
            return str(obj.province_id.code)
        else:
            return None

    def get_district_code(self, obj):
        if obj.district_id:
            return str(obj.district_id.code)
        else:
            return None

    def get_municipality_code(self, obj):
        if obj.municipality_id:
            return str(obj.municipality_id.code)
        else:
            return None

    def get_budget(self, obj):
        if obj.budget:
            return int(obj.budget)
        else:
            return None


class CovidSpecificBudgetSerializer(serializers.ModelSerializer):
    program = CovidSpecificSerializer(many=True, read_only=True)

    class Meta:
        model = CovidSpecificProgramBudget
        fields = (
            'id', 'total_budget', 'unallocated', 'reported', 'difference', 'percentage_reported',
            'percentage_unreported',
            'program')


class DryDshosp4hrUncoveredAdm1SumsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DryDshosp4hrUncoveredAdm1Sums
        fields = '__all__'


class DryDshosp8hrSumsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DryDshosp8hrSums
        fields = '__all__'


class DryDshosp8hrUncoveredAdm1SumsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DryDshosp8hrUncoveredAdm1Sums
        fields = '__all__'


class DryDshosp12hrSumsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DryDshosp12hrSums
        fields = '__all__'


class DryDshosp12hrUncoveredAdm1SumsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DryDshosp12hrUncoveredAdm1Sums
        fields = '__all__'


class DryAllCovidsDhfs4hrSumsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DryAllCovidsDhfs4hrSums
        fields = '__all__'


class DryAllCovidsDhfs4hrUncoveredAdm1SumsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DryAllCovidsDhfs4hrUncoveredAdm1Sums
        fields = '__all__'


class DryAllCovidsDhfs8hrSumsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DryAllCovidsDhfs8hrSums
        fields = '__all__'


class DryAllCovidsDhfs8hrUncoveredAdm1SumsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DryAllCovidsDhfs8hrUncoveredAdm1Sums
        fields = '__all__'


class DryAllCovidsDhfs12hrSumsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DryAllCovidsDhfs12hrSums
        fields = '__all__'


class DryAllCovidsDhfs12hrUncoveredAdm1SumsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DryAllCovidsDhfs12hrUncoveredAdm1Sums
        fields = '__all__'
