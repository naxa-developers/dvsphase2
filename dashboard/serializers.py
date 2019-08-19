from rest_framework import serializers
from .models import FiveW

class FivewSerializer(serializers.ModelSerializer):
    class Meta:
        model = FiveW
        fields= ('__all__')
