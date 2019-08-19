from django.db import models
from core.models import Program,Partner
# Create your models here.

class FiveW(models.Model):
    partner_name=models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='Partner', null=True, blank=True)
    program_name=models.ForeignKey(Program, on_delete=models.CASCADE, related_name='Program', null=True, blank=True)


    def __str__(self):
        return self.partner_name
