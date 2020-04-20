from rest_framework import serializers
from .models import Ttmp


class TtmpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ttmp
        fields = '__all__'
