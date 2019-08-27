from django.db import models


# Create your models here.
class Partner(models.Model):
    partner_name = models.CharField(max_length=100, null=True, blank=True)
    partner_description = models.TextField(null=True, blank=True)
    partner_address = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.partner_name


class MarkerCategory(models.Model):
    marker_category = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.marker_category


class MarkerValues(models.Model):
    marker_category = models.ForeignKey(MarkerCategory, on_delete=models.CASCADE, related_name='MarkerCategory',
                                        null=True, blank=True)
    marker_values = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return "{}-{}".format(self.marker_category, self.marker_values)


class Sector(models.Model):
    sector_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.sector_name


class SubSector(models.Model):
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='Sector', null=True, blank=True)
    sub_sector_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.sub_sector_name


class Program(models.Model):
    program_name = models.CharField(max_length=100, null=True, blank=True)
    program_description = models.TextField(blank=True)
    sub_sector = models.ForeignKey(SubSector, on_delete=models.CASCADE, related_name='SubSector', null=True, blank=True)
    marker = models.ManyToManyField(MarkerValues, related_name='MarkerValues', blank=True)
    program_code = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.program_name


class Province(models.Model):
    province_name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.province_name


class District(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='DProvince', null=True, blank=True)
    district_name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.district_name


class GapaNapa(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='Province', null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='District', null=True, blank=True)
    gapaNapa_name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.gapaNapa_name


class FiveW(models.Model):
    partner_name = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='Partner', null=True, blank=True)
    program_name = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='Program', null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='FProvince', null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='FDistrict', null=True, blank=True)
    gapa_napa = models.ForeignKey(GapaNapa, on_delete=models.CASCADE, related_name='GapaNapa', null=True, blank=True)
    implenting_partner_first = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='FPartner', null=True,
                                                 blank=True)
    implenting_partner_second = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='SPartner', null=True,
                                                  blank=True)
    implenting_partner_third = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='TPartner', null=True,
                                                 blank=True)
    implenting_partner_fourth = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='FOPartner',
                                                  null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.CharField(max_length=100, null=True, blank=True)
    end_date = models.CharField(max_length=100, null=True, blank=True)
    reporting_ministry_line = models.CharField(max_length=100, null=True, blank=True)
    budget = models.FloatField(null=True, blank=True, default=None)
    rp_name = models.CharField(max_length=200, null=True, blank=True)
    rp_contact_name = models.CharField(max_length=200, null=True, blank=True)
    rp_email = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return self.partner_name.partner_name
