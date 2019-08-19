from django.db import models
from core.models import Program,Partner
# Create your models here.

class FiveW(models.Model):
    partner_name=models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='Partner', null=True, blank=True)
    program_name=models.ForeignKey(Program, on_delete=models.CASCADE, related_name='Program', null=True, blank=True)
    province=models.CharField(max_length=100,null=True,blank=True)
    district=models.CharField(max_length=100,null=True,blank=True)
    gapa_napa=models.CharField(max_length=100,null=True,blank=True)
    status=models.CharField(max_length=100,null=True,blank=True)
    start_date=models.CharField(max_length=100,null=True,blank=True)
    end_date=models.CharField(max_length=100,null=True,blank=True)
    reporting_ministry_line=models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.partner_name.partner_name
