from django.contrib.gis.db import models


# Create your models here.
class Partner(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    type_of_institution = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    # contact_person_name = models.CharField(max_length=100, null=True, blank=True)
    # contact_person_email = models.CharField(max_length=100, null=True, blank=True)
    # contact_person_ph = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='upload/partner/', null=True, blank=True)

    def __str__(self):
        return self.name


class PartnerContact(models.Model):
    partner_id = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='PartnerContact')
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class MarkerCategory(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class MarkerValues(models.Model):
    marker_category_id = models.ForeignKey(MarkerCategory, on_delete=models.CASCADE, related_name='MarkerCategory')

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
        return "{}--{}".format(self.sector_id, self.name)


class Program(models.Model):
    status = (
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),

    )

    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(blank=True)
    sector = models.ManyToManyField(Sector, related_name='Psector', blank=True)
    sub_sector = models.ManyToManyField(SubSector, related_name='SubSector', blank=True)
    marker_category = models.ManyToManyField(MarkerCategory, related_name='Pmarkercategory', blank=True)
    marker_value = models.ManyToManyField(MarkerValues, related_name='MarkerValues', blank=True)
    partner = models.ManyToManyField(Partner, related_name='Ppartner', blank=True)
    program_code = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=50, choices=status, default='ongoing')
    budget = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Province(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class District(models.Model):
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='DProvince', null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    boundary = models.MultiPolygonField(srid=4326, null=True)

    def __str__(self):
        return self.name


class GapaNapa(models.Model):
    geog = (
        ('Terai', 'Terai'),
        ('Hill', 'Hill'),
        ('Shivalik', 'Shivalik'),
        ('Mountain', 'Mountain'),
        ('High Mountain', 'High Mountain'),
    )

    gn_en = (
        ('Rural municipality', 'Rural municipality'),
        ('Urban municipality', 'Urban municipality'),
        ('Designated area', 'Designated area'),
        ('Sub metropolitan', 'Sub metropolitan'),
        ('Metropolitan', 'Metropolitan'),
    )

    gn_nep = (
        ('Development area', 'Development area'),
        ('Gaunpalika', 'Gaunpalika'),
        ('Hunting reserve', 'Hunting reserve'),
        ('Nagarpalika', 'Nagarpalika'),
        ('Mahanagarpalika', 'Mahanagarpalika'),
        ('Upamahanagarpalika', 'Upamahanagarpalika'),
        ('Wildlife reserve', 'Wildlife reserve'),
        ('Watershed and wildlife reserve', 'Watershed and wildlife reserve'),
    )

    province_id = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='Province', null=True, blank=True)
    district_id = models.ForeignKey(District, on_delete=models.CASCADE, related_name='District', null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    gn_type_en = models.CharField(max_length=50, choices=gn_en, default='Rural municipality')
    gn_type_np = models.CharField(max_length=50, choices=gn_nep, default='Gaunpalika')
    population = models.FloatField(null=True, blank=True)
    geography = models.CharField(max_length=50, choices=geog, default='Terai')
    cbs_code = models.CharField(max_length=100, null=True, blank=True)
    hlcit_code = models.CharField(max_length=100, null=True, blank=True)
    p_code = models.CharField(max_length=100, null=True, blank=True)
    boundary = models.MultiPolygonField(srid=4326, null=True)

    def __str__(self):
        return self.name


class FiveW(models.Model):
    status = (
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),

    )

    partner_id = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='Partner', null=True, blank=True)
    program_id = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='Program', null=True, blank=True)
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='FProvince', null=True, blank=True)
    district_id = models.ForeignKey(District, on_delete=models.CASCADE, related_name='FDistrict', null=True, blank=True)
    municipality_id = models.ForeignKey(GapaNapa, on_delete=models.CASCADE, related_name='GapaNapa', null=True,
                                        blank=True)
    ward = models.CharField(max_length=200, null=True, blank=True)
    consortium_partner_first_id = models.ForeignKey(Partner, on_delete=models.CASCADE,
                                                    related_name='ConsortiumPartnerF',
                                                    null=True, blank=True)
    consortium_partner_second_id = models.ForeignKey(Partner, on_delete=models.CASCADE,
                                                     related_name='ConsortiumPartnerS',
                                                     null=True, blank=True)
    consortium_partner_third_id = models.ForeignKey(Partner, on_delete=models.CASCADE,
                                                    related_name='ConsortiumPartnerT',
                                                    null=True, blank=True)
    implementing_partner_first_id = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='FPartner',
                                                      null=True,
                                                      blank=True)
    implementing_partner_second_id = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='SPartner',
                                                       null=True,
                                                       blank=True)
    implementing_partner_third_id = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='TPartner',
                                                      null=True,
                                                      blank=True)
    implementing_partner_fourth_id = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='FOPartner',
                                                       null=True, blank=True)
    local_partner_first_id = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='LocalPartnerF',
                                               null=True, blank=True)
    local_partner_second_id = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='LocalPartnerS',
                                                null=True, blank=True)
    local_partner_third_id = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='LocalPartnerT',
                                               null=True, blank=True)
    status = models.CharField(max_length=50, choices=status, default='ongoing')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    reporting_ministry_line = models.CharField(max_length=100, null=True, blank=True)
    budget = models.FloatField(null=True, blank=True, default=None)
    representative_person = models.ForeignKey(PartnerContact, on_delete=models.CASCADE, related_name='PartnerContact',
                                              null=True,
                                              blank=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return self.partner_id.name


class Indicator(models.Model):
    fed = (
        ('palika level', 'Palika Level'),
        ('district level', 'District Level'),
        ('province level', 'Province Level'),
    )

    indicator = models.CharField(max_length=100, null=True, blank=True)
    full_title = models.CharField(max_length=500, null=True, blank=True)
    abstract = models.CharField(max_length=1500, null=True, blank=True)
    category = models.CharField(max_length=500, null=True, blank=True)
    source = models.CharField(max_length=1500, null=True, blank=True)
    federal_level = models.CharField(max_length=50, choices=fed, default='palika level')

    def __str__(self):
        return self.indicator


class IndicatorValue(models.Model):
    indicator_id = models.ForeignKey(Indicator, on_delete=models.CASCADE, related_name='Indicator', null=True,
                                     blank=True)
    gapanapa_id = models.ForeignKey(GapaNapa, on_delete=models.CASCADE, related_name='IgapaNapa', null=True, blank=True)
    value = models.FloatField(null=True, blank=True, default=None)

    def __str__(self):
        return self.indicator_id


class TravelTime(models.Model):
    gapanapa = models.ForeignKey(GapaNapa, on_delete=models.CASCADE, related_name='TgapaNapa', null=True, blank=True)
    facility_type = models.CharField(max_length=100, null=True, blank=True)
    travel_category_population = models.FloatField(null=True, blank=True, default=None)
    tc_pc_pop = models.FloatField(null=True, blank=True, default=None)
    season = models.CharField(max_length=100, null=True, blank=True)
    travel_category = models.CharField(max_length=100, null=True, blank=True)


class GisLayer(models.Model):
    type = (
        ('vector', 'Vector'),
        ('raster', 'Raster'),

    )

    name = models.CharField(max_length=100, null=True, blank=True)
    layer_name = models.CharField(max_length=100, null=True, blank=True)
    workspace = models.CharField(max_length=100, null=True, blank=True)
    geoserver_url = models.CharField(max_length=300, null=True, blank=True)
    store_name = models.CharField(max_length=300, null=True, blank=True)
    type = models.CharField(max_length=50, choices=type, default='vector')
    category = models.CharField(max_length=100, null=True, blank=True)
    filename = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    program_id = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='ProjectProgram', null=True,
                                   blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Output(models.Model):
    indicator = models.CharField(max_length=100, null=True, blank=True)
    male_forecast_2011_2015 = models.IntegerField(null=True, blank=True, default=0)
    female_forecast_2011_2015 = models.IntegerField(null=True, blank=True, default=0)
    male_achieved_2011_2015 = models.IntegerField(null=True, blank=True, default=0)
    female_achieved_2011_2015 = models.IntegerField(null=True, blank=True, default=0)
    male_forecast_2015_2019 = models.IntegerField(null=True, blank=True, default=0)
    female_forecast_2015_2019 = models.IntegerField(null=True, blank=True, default=0)
    male_achieved_2015_2019 = models.IntegerField(null=True, blank=True, default=0)
    female_achieved_2015_2019 = models.IntegerField(null=True, blank=True, default=0)
    male_forecast_2011_2019 = models.IntegerField(null=True, blank=True, default=0)
    female_forecast_2011_2019 = models.IntegerField(null=True, blank=True, default=0)
    male_achieved_2011_2019 = models.IntegerField(null=True, blank=True, default=0)
    female_achieved_2011_2019 = models.IntegerField(null=True, blank=True,  default=0)

    def __str__(self):
        return self.indicator

    @property
    def total_forecast_2011_2015(self):
        return self.male_forecast_2011_2015 + self.female_forecast_2011_2015

    @property
    def total_achieved_2011_2015(self):
        return self.male_achieved_2011_2015 + self.female_achieved_2011_2015

    @property
    def total_forecast_2015_2019(self):
        return self.male_forecast_2015_2019 + self.female_forecast_2015_2019

    @property
    def total_achieved_2015_2019(self):
        return self.male_achieved_2015_2019 + self.female_achieved_2015_2019

    @property
    def total_forecast_2011_2019(self):
        return self.male_forecast_2011_2019 + self.female_forecast_2011_2019

    @property
    def total_achieved_2011_2019(self):
        return self.male_achieved_2011_2019 + self.female_achieved_2011_2019
