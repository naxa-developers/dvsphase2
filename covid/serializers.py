from rest_framework import serializers
from .models import CovidFivew, DryDshosp4hrSums, DryDshosp4hrUncoveredAdm1Sums, DryDshosp8hrSums, \
    DryDshosp8hrUncoveredAdm1Sums, DryDshosp12hrSums, DryDshosp12hrUncoveredAdm1Sums, DryAllCovidsDhfs4hrSums, \
    DryAllCovidsDhfs4hrUncoveredAdm1Sums, DryAllCovidsDhfs8hrSums, DryAllCovidsDhfs8hrUncoveredAdm1Sums, \
    DryAllCovidsDhfs12hrSums, DryAllCovidsDhfs12hrUncoveredAdm1Sums


class CovidFivewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CovidFivew
        fields = '__all__'


class DryDshosp4hrSumsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DryDshosp4hrSums
        fields = '__all__'


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
