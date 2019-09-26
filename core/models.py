from django.contrib.gis.db import models


# Create your models here.
class Partner(models.Model):
    partner_name = models.CharField(max_length=100, null=True, blank=True)
    partner_description = models.TextField(null=True, blank=True)
    partner_address = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.partner_name


class MarkerCategory(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class MarkerValues(models.Model):
    marker_category_id = models.ForeignKey(MarkerCategory, on_delete=models.CASCADE, related_name='MarkerCategory',
                                        null=True, blank=True)
    value = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return "{}-{}".format(self.marker_category_id, self.value)


class Sector(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class SubSector(models.Model):
    sector_id = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='Sector', null=True, blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    code = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "{}--{}".format(self.sector, self.sub_sector_name)


class Program(models.Model):
    program_name = models.CharField(max_length=100, null=True, blank=True)
    program_description = models.TextField(blank=True)
    sector = models.ManyToManyField(Sector, related_name='Psector', blank=True)
    sub_sector = models.ManyToManyField(SubSector, related_name='SubSector', blank=True)
    marker_category = models.ManyToManyField(MarkerCategory, related_name='Pmarkercategory', blank=True)
    marker_value = models.ManyToManyField(MarkerValues, related_name='MarkerValues', blank=True)
    program_code = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.program_name


class Province(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class District(models.Model):
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='DProvince', null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class GapaNapa(models.Model):
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='Province', null=True, blank=True)
    district_id = models.ForeignKey(District, on_delete=models.CASCADE, related_name='District', null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    gn_type_en = models.CharField(max_length=100, null=True, blank=True)
    gn_type_np = models.CharField(max_length=100, null=True, blank=True)
    population = models.FloatField(null=True, blank=True)
    geography = models.CharField(max_length=100, null=True, blank=True)
    cbs_code = models.CharField(max_length=100, null=True, blank=True)
    hlcit_code = models.CharField(max_length=100, null=True, blank=True)
    p_code = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


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


class Indicator(models.Model):
    indicator = models.CharField(max_length=100, null=True, blank=True)
    full_title = models.CharField(max_length=500, null=True, blank=True)
    abstract = models.CharField(max_length=1500, null=True, blank=True)
    category = models.CharField(max_length=500, null=True, blank=True)
    source = models.CharField(max_length=1500, null=True, blank=True)
    federal_level = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.indicator


class IndicatorValue(models.Model):
    indicator_id = models.ForeignKey(Indicator, on_delete=models.CASCADE, related_name='Indicator', null=True, blank=True)
    gapanapa_id = models.ForeignKey(GapaNapa, on_delete=models.CASCADE, related_name='IgapaNapa', null=True, blank=True)
    value = models.FloatField(null=True, blank=True, default=None)

    def __float__(self):
        return self.value


class TravelTime(models.Model):
    gapanapa = models.ForeignKey(GapaNapa, on_delete=models.CASCADE, related_name='TgapaNapa', null=True, blank=True)
    facility_type = models.CharField(max_length=100, null=True, blank=True)
    travel_category_population = models.FloatField(null=True, blank=True, default=None)
    tc_pc_pop = models.FloatField(null=True, blank=True, default=None)
    season = models.CharField(max_length=100, null=True, blank=True)
    travel_category = models.CharField(max_length=100, null=True, blank=True)
