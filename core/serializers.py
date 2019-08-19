from rest_framework import serializers
from .models import Partner,Program,MarkerValues,MarkerCategory

class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields= ('__all__')


class MarkerCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model=MarkerCategory
        fields= ('__all__')

class MarkerValuesSerializer(serializers.ModelSerializer):
    marker_category=serializers.SerializerMethodField()
    class Meta:
        model = MarkerValues
        fields= ('marker_values','marker_category')

    def get_marker_category(self,obj):
         return str(obj.marker_category.marker_category)

class ProgramSerializer(serializers.ModelSerializer):
    marker=serializers.SerializerMethodField()
    sub_sector=serializers.SerializerMethodField()
    class Meta:
        model=Program
        fields=('program_name','program_description','sub_sector','marker')

    def get_marker(self,obj):
         qs = obj.marker.all().order_by('id')
         return MarkerValuesSerializer(qs, many=True, read_only=True).data

    def get_sub_sector(self,obj):
        return str(obj.sub_sector.sub_sector_name)
