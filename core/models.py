from django.contrib.gis.db import models
from django.contrib.auth.models import User
import os.path
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
from colorfield.fields import ColorField
from ckeditor.fields import RichTextField


# Create your models here

class Partner(models.Model):
    type_of_institution = (
        ('Government', 'Government'),
        ('International NGO', 'International NGO'),
        ('National NGO', 'National NGO'),
        ('Multilateral', 'Multilateral'),
        ('Private Sector', 'Private Sector'),
        ('Local Government', 'Local Government'),
        ('Other Public Sector', 'Other Public Sector'),
        ('Regional NGO', 'Regional NGO'),
        ('Partner Country based NGO', 'Partner Country based NGO'),
        ('Public Private Partnership', 'Public Private Partnership'),
        ('Foundation', 'Foundation'),
        ('Private Sector in Provider Country', 'Private Sector in Provider Country'),
        ('Academic, Training and Research', 'Academic, Training and Research'),
        ('Private Sector in Aid Recipient Country', 'Private Sector in Aid Recipient Country'),
        ('Private Sector in Third Country', 'Private Sector in Third Country'),
        ('Academic, Training and Research', 'Academic, Training and Research'),
        ('Other', 'Other')
    )
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    type_of_institution = models.CharField(max_length=100, choices=type_of_institution, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='upload/partner/', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='upload/partner/', editable=False, null=True, blank=True)
    code = models.IntegerField(blank=True, null=True)

    def make_thumbnail(self):
        try:
            image = Image.open(self.image)
            print(image)
            image.thumbnail((200, 150), Image.ANTIALIAS)
            thumb_name, thumb_extension = os.path.splitext(self.image.name)
            thumb_extension = thumb_extension.lower()
            thumb_filename = thumb_name + '_thumb' + thumb_extension
            if thumb_extension in ['.jpg', '.jpeg']:
                FTYPE = 'JPEG'
            elif thumb_extension == '.gif':
                FTYPE = 'GIF'
            elif thumb_extension == '.png':
                FTYPE = 'PNG'
            else:
                return False  # Unrecognized file type
            # Save thumbnail to in-memory file as StringIO
            temp_thumb = BytesIO()
            image.save(temp_thumb, FTYPE)
            temp_thumb.seek(0)
            # set save=False, otherwise it will run in an infinite loop
            self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
            temp_thumb.close()
            return True
        except:
            return False

    def save(self, *args, **kwargs):
        if not self.make_thumbnail():
            print('ok')
            # set to a default thumbnail
            # raise Exception('Could not create thumbnail - is the file type valid?')
        super(Partner, self).save(*args, **kwargs)

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
    partner_id = models.ManyToManyField(Partner, related_name='Progpartner')
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    cmp = models.BooleanField(blank=True, null=True)
    code = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=50, choices=status, default='ongoing')
    total_budget = models.FloatField(null=True, blank=True, default=0)
    budget_spend = models.FloatField(null=True, blank=True, default=0)
    marker_category = models.ManyToManyField(MarkerCategory, related_name='Pmarkercategory', blank=True)
    marker_value = models.ManyToManyField(MarkerValues, related_name='MarkerValues', blank=True)
    sector = models.ManyToManyField(Sector, related_name='Progsector', blank=True)
    sub_sector = models.ManyToManyField(SubSector, related_name='ProgSubSector', blank=True)
    sector_budget = models.TextField(blank=True, null=True)
    iati = models.CharField(max_length=100, blank=True, null=True)
    program_acronym = models.CharField(max_length=1500, blank=True, null=True)

    def __str__(self):
        return self.name


class Province(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    bbox = models.CharField(max_length=600, null=True, blank=True)

    def __str__(self):
        return self.name


class District(models.Model):
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='DProvince', null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    n_code = models.IntegerField(null=True, blank=True)
    bbox = models.CharField(max_length=600, null=True, blank=True)

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
    hlcit_code = models.CharField(max_length=500, null=True, blank=True)
    p_code = models.CharField(max_length=100, null=True, blank=True)
    code = models.IntegerField(null=True, blank=True)
    bbox = models.CharField(max_length=600, null=True, blank=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    program_id = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='ProjectProgram', null=True,
                                   blank=True)
    partner_id = models.ManyToManyField(Partner, related_name='ProjectPartner', blank=True, null=True)
    name = models.CharField(max_length=500, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    federal_intervention = models.BooleanField(blank=True, null=True)
    sector = models.ManyToManyField(Sector, related_name='Psector', blank=True)
    sub_sector = models.ManyToManyField(SubSector, related_name='SubSector', blank=True)
    component_acronym = models.CharField(max_length=1500, blank=True, null=True)
    approved_budget = models.FloatField(blank=True, null=True)
    budget_spend = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name


class FiveW(models.Model):
    status = (
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),

    )

    ktm = (
        ('Intervention', 'Intervention'),
        ('Influence', 'Influence'),
        ('N/A', 'N/A'),

    )

    c_other = (
        ('NA - Complete', 'NA - Complete'),
        ('Yes', 'Yes'),
        ('Partial High', 'Partial High'),
        ('Partial Low', 'Partial Low'),
        ('No', 'No'),

    )

    admin_level = (
        ('national', 'National'),
        ('province', 'Province'),
        ('district', 'District'),
        ('municipality', 'Municipality'),

    )

    supplier_id = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='Partner', null=True, blank=True)
    second_tier_partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='SPartner', null=True,
                                            blank=True)
    second_tier_partner_name = models.CharField(max_length=3500, null=True, blank=True)
    program_id = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='Program', null=True, blank=True)
    component_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='FProject', null=True, blank=True)
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='FProvince', null=True, blank=True)
    district_id = models.ForeignKey(District, on_delete=models.CASCADE, related_name='FDistrict', null=True, blank=True)
    municipality_id = models.ForeignKey(GapaNapa, on_delete=models.CASCADE, related_name='GapaNapa', null=True,
                                        blank=True)
    status = models.CharField(max_length=1500, choices=status, default='ongoing')
    allocated_budget = models.FloatField(null=True, blank=True, default=0)
    kathmandu_activity = models.CharField(max_length=500, choices=ktm, blank=True, null=True, default='N/A')
    delivery_in_lockdown = models.CharField(max_length=500, choices=c_other, blank=True, null=True, default='No')
    covid_priority_3_12_Months = models.CharField(max_length=500, choices=c_other, blank=True, null=True, default='No')
    covid_recovery_priority = models.CharField(max_length=500, choices=c_other, blank=True, null=True, default='No')
    providing_ta_to_local_government = models.CharField(max_length=500, choices=c_other, blank=True, null=True,
                                                        default='No')
    providing_ta_to_provincial_government = models.CharField(max_length=500, choices=c_other, blank=True, null=True,
                                                             default='No')
    reporting_line_ministry = models.CharField(max_length=1500, blank=True, null=True)
    contact_name = models.CharField(max_length=500, blank=True, null=True)
    designation = models.CharField(max_length=1500, blank=True, null=True)
    contact_number = models.CharField(max_length=500, blank=True, null=True)
    email = models.CharField(max_length=500, blank=True, null=True)
    remarks = models.CharField(max_length=1500, blank=True, null=True)

    def __str__(self):
        return self.supplier_id.name


class Indicator(models.Model):
    fed = (
        ('all', 'All'),
        ('palika', 'Palika Level'),
        ('district', 'District Level'),
        ('province', 'Province Level'),
    )

    indicator = models.CharField(max_length=100, null=True, blank=True)
    full_title = models.CharField(max_length=500, null=True, blank=True)
    abstract = models.CharField(max_length=1500, null=True, blank=True)
    category = models.CharField(max_length=500, null=True, blank=True)
    source = models.CharField(max_length=1500, null=True, blank=True)
    url = models.CharField(max_length=1500, null=True, blank=True)
    federal_level = models.CharField(max_length=50, choices=fed, default='all')
    is_covid = models.BooleanField(default=True)
    show_flag = models.BooleanField(default=True)
    unit = models.CharField(max_length=1500, null=True, blank=True)
    data_type = models.CharField(max_length=1500, null=True, blank=True)
    is_dashboard = models.BooleanField(default=True)
    is_regional_profile = models.BooleanField(default=True)

    def __str__(self):
        return self.indicator


class IndicatorValue(models.Model):
    indicator_id = models.ForeignKey(Indicator, on_delete=models.CASCADE, related_name='Indicator', null=True,
                                     blank=True)
    gapanapa_id = models.ForeignKey(GapaNapa, on_delete=models.CASCADE, related_name='IgapaNapa', null=True, blank=True)
    value = models.FloatField(default=0)
    district_id = models.ForeignKey(District, on_delete=models.CASCADE, related_name='Idistrict', null=True, blank=True)
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='Iprovince', null=True, blank=True)
    national_average = models.FloatField(default=0)
    province_average = models.FloatField(default=0)
    district_average = models.FloatField(default=0)

    def __str__(self):
        return self.indicator_id.indicator


class Filter(models.Model):
    indicator_id = models.ForeignKey(Indicator, on_delete=models.CASCADE, related_name='filter', null=True,
                                     blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    options = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name


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
    geo_type = models.CharField(max_length=100, null=True, blank=True)
    filename = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    identifier_key = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class GisStyle(models.Model):
    circle_color = ColorField(default='#FF0000', blank=True, null=True)
    fill_color = ColorField(default='#FF0000', blank=True, null=True)
    circle_radius = models.FloatField(blank=True, null=True)
    layer = models.ForeignKey(GisLayer, on_delete=models.CASCADE, related_name='GisStyle', blank=True, null=True)

    def __str__(self):
        return self.layer.name


class GisPop(models.Model):
    key = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    layer = models.ForeignKey(GisLayer, on_delete=models.CASCADE, related_name='GisPop', blank=True, null=True)

    def __str__(self):
        return self.layer.name


class Output(models.Model):
    indicator = models.CharField(max_length=100, null=True, blank=True)
    male_forecast_2011 = models.IntegerField(null=True, blank=True, default=0)
    disability_forecast_2011 = models.IntegerField(null=True, blank=True, default=0)
    female_forecast_2011 = models.IntegerField(null=True, blank=True, default=0)
    total_forecast_2011 = models.IntegerField(null=True, blank=True, default=0)
    male_achieved_2011 = models.IntegerField(null=True, blank=True, default=0)
    female_achieved_2011 = models.IntegerField(null=True, blank=True, default=0)
    disability_achieved_2011 = models.IntegerField(null=True, blank=True, default=0)
    total_achieved_2011 = models.IntegerField(null=True, blank=True, default=0)
    male_forecast_2012 = models.IntegerField(null=True, blank=True, default=0)
    female_forecast_2012 = models.IntegerField(null=True, blank=True, default=0)
    disability_forecast_2012 = models.IntegerField(null=True, blank=True, default=0)
    total_forecast_2012 = models.IntegerField(null=True, blank=True, default=0)
    male_achieved_2012 = models.IntegerField(null=True, blank=True, default=0)
    female_achieved_2012 = models.IntegerField(null=True, blank=True, default=0)
    disability_achieved_2012 = models.IntegerField(null=True, blank=True, default=0)
    total_achieved_2012 = models.IntegerField(null=True, blank=True, default=0)
    male_forecast_2013 = models.IntegerField(null=True, blank=True, default=0)
    female_forecast_2013 = models.IntegerField(null=True, blank=True, default=0)
    disability_forecast_2013 = models.IntegerField(null=True, blank=True, default=0)
    total_forecast_2013 = models.IntegerField(null=True, blank=True, default=0)
    male_achieved_2013 = models.IntegerField(null=True, blank=True, default=0)
    female_achieved_2013 = models.IntegerField(null=True, blank=True, default=0)
    disability_achieved_2013 = models.IntegerField(null=True, blank=True, default=0)
    total_achieved_2013 = models.IntegerField(null=True, blank=True, default=0)
    male_forecast_2014 = models.IntegerField(null=True, blank=True, default=0)
    female_forecast_2014 = models.IntegerField(null=True, blank=True, default=0)
    disability_forecast_2014 = models.IntegerField(null=True, blank=True, default=0)
    total_forecast_2014 = models.IntegerField(null=True, blank=True, default=0)
    male_achieved_2014 = models.IntegerField(null=True, blank=True, default=0)
    female_achieved_2014 = models.IntegerField(null=True, blank=True, default=0)
    disability_achieved_2014 = models.IntegerField(null=True, blank=True, default=0)
    total_achieved_2014 = models.IntegerField(null=True, blank=True, default=0)
    male_forecast_2015 = models.IntegerField(null=True, blank=True, default=0)
    female_forecast_2015 = models.IntegerField(null=True, blank=True, default=0)
    disability_forecast_2015 = models.IntegerField(null=True, blank=True, default=0)
    total_forecast_2015 = models.IntegerField(null=True, blank=True, default=0)
    male_achieved_2015 = models.IntegerField(null=True, blank=True, default=0)
    female_achieved_2015 = models.IntegerField(null=True, blank=True, default=0)
    disability_achieved_2015 = models.IntegerField(null=True, blank=True, default=0)
    total_achieved_2015 = models.IntegerField(null=True, blank=True, default=0)
    male_forecast_2016 = models.IntegerField(null=True, blank=True, default=0)
    female_forecast_2016 = models.IntegerField(null=True, blank=True, default=0)
    disability_forecast_2016 = models.IntegerField(null=True, blank=True, default=0)
    total_forecast_2016 = models.IntegerField(null=True, blank=True, default=0)
    male_achieved_2016 = models.IntegerField(null=True, blank=True, default=0)
    female_achieved_2016 = models.IntegerField(null=True, blank=True, default=0)
    disability_achieved_2016 = models.IntegerField(null=True, blank=True, default=0)
    total_achieved_2016 = models.IntegerField(null=True, blank=True, default=0)
    male_forecast_2017 = models.IntegerField(null=True, blank=True, default=0)
    female_forecast_2017 = models.IntegerField(null=True, blank=True, default=0)
    disability_forecast_2017 = models.IntegerField(null=True, blank=True, default=0)
    total_forecast_2017 = models.IntegerField(null=True, blank=True, default=0)
    male_achieved_2017 = models.IntegerField(null=True, blank=True, default=0)
    female_achieved_2017 = models.IntegerField(null=True, blank=True, default=0)
    disability_achieved_2017 = models.IntegerField(null=True, blank=True, default=0)
    total_achieved_2017 = models.IntegerField(null=True, blank=True, default=0)
    male_forecast_2018 = models.IntegerField(null=True, blank=True, default=0)
    female_forecast_2018 = models.IntegerField(null=True, blank=True, default=0)
    disability_forecast_2018 = models.IntegerField(null=True, blank=True, default=0)
    total_forecast_2018 = models.IntegerField(null=True, blank=True, default=0)
    male_achieved_2018 = models.IntegerField(null=True, blank=True, default=0)
    female_achieved_2018 = models.IntegerField(null=True, blank=True, default=0)
    disability_achieved_2018 = models.IntegerField(null=True, blank=True, default=0)
    total_achieved_2018 = models.IntegerField(null=True, blank=True, default=0)
    male_forecast_2019 = models.IntegerField(null=True, blank=True, default=0)
    female_forecast_2019 = models.IntegerField(null=True, blank=True, default=0)
    disability_forecast_2019 = models.IntegerField(null=True, blank=True, default=0)
    total_forecast_2019 = models.IntegerField(null=True, blank=True, default=0)
    male_achieved_2019 = models.IntegerField(null=True, blank=True, default=0)
    female_achieved_2019 = models.IntegerField(null=True, blank=True, default=0)
    disability_achieved_2019 = models.IntegerField(null=True, blank=True, default=0)
    total_achieved_2019 = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.indicator


class ProvinceDummy(models.Model):
    province_id = models.IntegerField(blank=True, null=True)
    geom_char = models.TextField(blank=True, null=True)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='User', null=True, blank=True)
    message = models.CharField(max_length=500, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    link = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(auto_now_add=True)


class BudgetToSecondTier(models.Model):
    supplier_id = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='BsPartner', null=True, )
    second_tier_partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='BPartner', null=True, )
    program_id = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='BProgram', null=True, blank=True)
    component_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='BProject', null=True, blank=True)
    contract_value = models.FloatField(null=True, blank=True, default=0)

    def __str__(self):
        return self.supplier_id.name


class BudgetToFirstTier(models.Model):
    supplier_id = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='BFPartner', null=True, )
    program_id = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='BFProgram', null=True, blank=True)
    component_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='BFProject', null=True, blank=True)
    approved_budget = models.FloatField(null=True, blank=True, default=0)
    spend_budget = models.FloatField(null=True, blank=True, default=0)

    def __str__(self):
        return self.supplier_id.name


class Cmp(models.Model):
    cat = (
        ('collaborate', 'Collaborate'),
        ('contribute', 'Contribute'),
        ('aware', 'Aware'),

    )

    project_code = models.CharField(max_length=100, null=True, blank=True)
    project_name = models.CharField(max_length=100, null=True, blank=True)
    total_project_budget = models.FloatField(null=True, blank=True, default=0)
    percentage_in_country = models.FloatField(null=True, blank=True, default=0)
    budget_country_fy = models.FloatField(null=True, blank=True, default=0)
    sro_name = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=50, choices=cat, null=True, blank=True)
    poc = models.CharField(max_length=100, null=True, blank=True)
    poc_email = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='CmProvince', null=True,
                                    blank=True)
    district_id = models.ForeignKey(District, on_delete=models.CASCADE, related_name='CmDistrict', null=True,
                                    blank=True)
    municipality_id = models.ForeignKey(GapaNapa, on_delete=models.CASCADE, related_name='CmGapaNapa', null=True)

    def __str__(self):
        return self.project_name


class NepalSummary(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    value = models.FloatField(null=True, blank=True, default=0)

    def __str__(self):
        return self.name


class FeedbackForm(models.Model):
    status = (
        ('New', 'New'),
        ('Old', 'Old'),
    )
    name = models.CharField(max_length=500, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    type = models.CharField(max_length=500, blank=True, null=True)
    subject = models.CharField(max_length=500, blank=True, null=True)
    your_feedback = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to='feedbackfiles', blank=True, null=True)
    status = models.CharField(max_length=500, choices=status, default='New')


class FAQ(models.Model):
    question = RichTextField(blank=True, null=True)
    answer = RichTextField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)


class TermsAndCondition(models.Model):
    title = RichTextField(blank=True, null=True)
    sub_title = RichTextField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)


class NationalStatistic(models.Model):
    title = models.CharField(max_length=500, blank=True, null=True)
    url = models.URLField(blank=True, null=True)


class Manual(models.Model):
    file = models.FileField(upload_to='feedbackfiles', blank=True, null=True)
