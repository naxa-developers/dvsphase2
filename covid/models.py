from django.db import models
from core.models import Province, District, GapaNapa


# Create your models here.


class CovidFivew(models.Model):
    partner = models.CharField(max_length=500, blank=True, null=True)
    supplier_code = models.CharField(max_length=100, blank=True, null=True)
    program = models.CharField(max_length=500, blank=True, null=True)
    project_name = models.CharField(max_length=500, blank=True, null=True)
    sector = models.CharField(max_length=500, blank=True, null=True)
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='TtmpProvince',
                                    null=True, blank=True)
    district_id = models.ForeignKey(District, on_delete=models.CASCADE, related_name='TtmpDistrict',
                                    null=True, blank=True)
    municipality_id = models.ForeignKey(GapaNapa, on_delete=models.CASCADE, related_name='TtmpGapaNapa',
                                        null=True, blank=True)
