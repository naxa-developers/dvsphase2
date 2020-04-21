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


class CommonField(models.Model):
    f_5 = models.CharField(max_length=20, blank=True, null=True)
    f_10 = models.CharField(max_length=20, blank=True, null=True)
    f_15 = models.CharField(max_length=20, blank=True, null=True)
    f_20 = models.CharField(max_length=20, blank=True, null=True)
    f_25 = models.CharField(max_length=20, blank=True, null=True)
    f_30 = models.CharField(max_length=20, blank=True, null=True)
    f_35 = models.CharField(max_length=20, blank=True, null=True)
    f_40 = models.CharField(max_length=20, blank=True, null=True)
    f_45 = models.CharField(max_length=20, blank=True, null=True)
    f_50 = models.CharField(max_length=20, blank=True, null=True)
    f_55 = models.CharField(max_length=20, blank=True, null=True)
    f_60 = models.CharField(max_length=20, blank=True, null=True)
    f_65 = models.CharField(max_length=20, blank=True, null=True)
    f_70 = models.CharField(max_length=20, blank=True, null=True)
    f_75 = models.CharField(max_length=20, blank=True, null=True)
    f_80 = models.CharField(max_length=20, blank=True, null=True)
    m_5 = models.CharField(max_length=20, blank=True, null=True)
    m_10 = models.CharField(max_length=20, blank=True, null=True)
    m_15 = models.CharField(max_length=20, blank=True, null=True)
    m_20 = models.CharField(max_length=20, blank=True, null=True)
    m_25 = models.CharField(max_length=20, blank=True, null=True)
    m_30 = models.CharField(max_length=20, blank=True, null=True)
    m_35 = models.CharField(max_length=20, blank=True, null=True)
    m_40 = models.CharField(max_length=20, blank=True, null=True)
    m_45 = models.CharField(max_length=20, blank=True, null=True)
    m_50 = models.CharField(max_length=20, blank=True, null=True)
    m_55 = models.CharField(max_length=20, blank=True, null=True)
    m_60 = models.CharField(max_length=20, blank=True, null=True)
    m_65 = models.CharField(max_length=20, blank=True, null=True)
    m_70 = models.CharField(max_length=20, blank=True, null=True)
    m_75 = models.CharField(max_length=20, blank=True, null=True)
    m_80 = models.CharField(max_length=20, blank=True, null=True)
    male_total = models.CharField(max_length=20, blank=True, null=True)
    female_total = models.CharField(max_length=20, blank=True, null=True)
    male_high_risk = models.CharField(max_length=20, blank=True, null=True)
    female_high_risk = models.CharField(max_length=20, blank=True, null=True)
    total = models.CharField(max_length=20, blank=True, null=True)
    all_high_risk = models.CharField(max_length=20, blank=True, null=True)
    all_risk_pct = models.CharField(max_length=20, blank=True, null=True)
    male_high_pct = models.CharField(max_length=20, blank=True, null=True)
    female_high_pct = models.CharField(max_length=20, blank=True, null=True)


class DryDeshospSum(CommonField):
    grid_code = models.CharField(max_length=20, blank=True, null=True)
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='DryDeshosp4hrSum',
                                    null=True, blank=True)
    district_id = models.ForeignKey(District, on_delete=models.CASCADE, related_name='DryDeshosp4hrSum',
                                    null=True, blank=True)
    municipality_id = models.ForeignKey(GapaNapa, on_delete=models.CASCADE, related_name='DryDeshosp4hrSum',
                                        null=True, blank=True)
    hospital_name = models.CharField(max_length=500, blank=True, null=True)
    category_code = models.CharField(max_length=10, blank=True, null=True)
    category_name = models.CharField(max_length=500, blank=True, null=True)
    type_code = models.CharField(max_length=10, blank=True, null=True)
    type_name = models.CharField(max_length=500, blank=True, null=True)
    ownership_code = models.CharField(max_length=10, blank=True, null=True)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    contact_num = models.CharField(max_length=100, blank=True, null=True)
    used_for_corona_response = models.CharField(max_length=100, blank=True, null=True)
    number_of_bed = models.CharField(max_length=10, blank=True, null=True)
    number_of_icu_bed = models.CharField(max_length=10, blank=True, null=True)
    occupied_icu_bed = models.CharField(max_length=10, blank=True, null=True)
    number_of_ventilators = models.CharField(max_length=10, blank=True, null=True)
    occupied_ventilators = models.CharField(max_length=10, blank=True, null=True)
    number_of_isolation_bed = models.CharField(max_length=10, blank=True, null=True)
    occupied_isolation_bed = models.CharField(max_length=10, blank=True, null=True)
    total_tested = models.CharField(max_length=10, blank=True, null=True)
    total_positive = models.CharField(max_length=10, blank=True, null=True)
    total_death = models.CharField(max_length=10, blank=True, null=True)
    total_in_isolation = models.CharField(max_length=10, blank=True, null=True)
    lat = models.CharField(max_length=20, blank=True, null=True)
    long = models.CharField(max_length=20, blank=True, null=True)


class DryDeshospUncoveredAdm1Sums(CommonField):
    object_code = models.CharField(max_length=20, blank=True, null=True)
    fid_adm1 = models.CharField(max_length=20, blank=True, null=True)
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='DryDeshosp4hrUncoveredAdm1Sums',
                                    null=True, blank=True)
    district_id = models.ForeignKey(District, on_delete=models.CASCADE, related_name='DryDeshosp4hrUncoveredAdm1Sums',
                                    null=True, blank=True)
    municipality_id = models.ForeignKey(GapaNapa, on_delete=models.CASCADE,
                                        related_name='DryDeshosp4hrUncoveredAdm1Sums', null=True, blank=True)
    sum_11 = models.CharField(max_length=20, blank=True, null=True)
    wp_sum = models.CharField(max_length=20, blank=True, null=True)
    hrsl_sum = models.CharField(max_length=20, blank=True, null=True)
    fid_dry_de = models.CharField(max_length=20, blank=True, null=True)
    object_id_1 = models.CharField(max_length=20, blank=True, null=True)
    palika_1 = models.CharField(max_length=500, blank=True, null=True)
    district_1 = models.CharField(max_length=500, blank=True, null=True)
    gapa_napa_1 = models.CharField(max_length=500, blank=True, null=True)
    province_1 = models.CharField(max_length=500, blank=True, null=True)
    shape_length = models.CharField(max_length=50, blank=True, null=True)
    shape_area = models.CharField(max_length=50, blank=True, null=True)
    uncov_id = models.CharField(max_length=50, blank=True, null=True)


class DryDshosp4hrSums(DryDeshospSum):
    data = models.CharField(max_length=100, blank=True, null=True)


class DryDshosp4hrUncoveredAdm1Sums(DryDeshospUncoveredAdm1Sums):
    data = models.CharField(max_length=100, blank=True, null=True)


class DryDshosp8hrSums(DryDeshospSum):
    data = models.CharField(max_length=100, blank=True, null=True)


class DryDshosp8hrUncoveredAdm1Sums(DryDeshospUncoveredAdm1Sums):
    data = models.CharField(max_length=100, blank=True, null=True)


class DryDshosp12hrSums(DryDeshospSum):
    data = models.CharField(max_length=100, blank=True, null=True)


class DryDshosp12hrUncoveredAdm1Sums(DryDeshospUncoveredAdm1Sums):
    data = models.CharField(max_length=100, blank=True, null=True)


class DryAllCovidsDhfs4hrSums(DryDeshospSum):
    data = models.CharField(max_length=100, blank=True, null=True)


class DryAllCovidsDhfs4hrUncoveredAdm1Sums(DryDeshospUncoveredAdm1Sums):
    data = models.CharField(max_length=100, blank=True, null=True)


class DryAllCovidsDhfs8hrSums(DryDeshospSum):
    data = models.CharField(max_length=100, blank=True, null=True)


class DryAllCovidsDhfs8hrUncoveredAdm1Sums(DryDeshospUncoveredAdm1Sums):
    data = models.CharField(max_length=100, blank=True, null=True)


class DryAllCovidsDhfs12hrSums(DryDeshospSum):
    data = models.CharField(max_length=100, blank=True, null=True)


class DryAllCovidsDhfs12hrUncoveredAdm1Sums(DryDeshospUncoveredAdm1Sums):
    data = models.CharField(max_length=100, blank=True, null=True)




