from django.db import models
from core.models import Program,Organization
# Create your models here.

class FiveW(models.Model):
    organization_name=models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='Organization', null=True, blank=True)
    program_name=models.ForeignKey(Program, on_delete=models.CASCADE, related_name='Program', null=True, blank=True)

    
