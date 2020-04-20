from django.db import models
from core.models import Partner, Program, Province, District, GapaNapa

# Create your models here.


class Ttmp(models.Model):
    partner_id = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='TtmpPartner',
                                   null=True, blank=True)
    supplier_id = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='TtmpSupplier',
                                    null=True, blank=True)
    program_id = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='TtmpProgram',
                                   null=True, blank=True)
    project_name = models.CharField(max_length=500, blank=True, null=True)
    project_code = models.CharField(max_length=50, blank=True, null=True)
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='TtmpProvince',
                                    null=True, blank=True)
    district_id = models.ForeignKey(District, on_delete=models.CASCADE, related_name='TtmpDistrict',
                                    null=True, blank=True)
    municipality_id = models.ForeignKey(GapaNapa, on_delete=models.CASCADE, related_name='TtmpGapaNapa',
                                        null=True, blank=True)

