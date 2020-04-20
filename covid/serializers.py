from rest_framework import serializers
from .models import CovidFivew


class CovidFivewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CovidFivew
        fields = '__all__'
