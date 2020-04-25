from django.core.management.base import BaseCommand
import pandas as pd
from core.models import GapaNapa, Province, District
from covid.models import DryDshosp8hrSums


class Command(BaseCommand):
    help = 'load province data from province.xlsx file'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']

        df = pd.read_csv(path, encoding='unicode_escape')
        upper_range = len(df)
        print("Wait Data is being Loaded")

        try:
            for row in range(0, upper_range):
                province = Province.objects.get(code=int(df['province_id'][row]))
                district = District.objects.get(code=int(df['district_id'][row]))
                municipality = GapaNapa.objects.get(hlcit_code=df['municipality_id'][row])

                DryDshosp8hrSums.objects.create(
                    grid_code=df['gridcode'][row],
                    province_id=province,
                    district_id=district,
                    municipality_id=municipality,
                    hospital_name=df['name'][row],
                    category_code=df['category'][row],
                    category_name=df['category__name'][row],
                    type_code=df['type'][row],
                    type_name=df['type__name'][row],
                    ownership_code=df['ownership'][row],
                    contact_person=df['contact_person'][row],
                    contact_num=df['contact_num'][row],
                    used_for_corona_response=df['used_for_corona_response'][row],
                    number_of_bed=df['num_of_bed'][row],
                    number_of_icu_bed=df['num_of_icu_bed'][row],
                    occupied_icu_bed=df['occupied_icu_bed'][row],
                    number_of_ventilators=df['num_of_ventilators'][row],
                    occupied_ventilators=df['occupied_ventilators'][row],
                    number_of_isolation_bed=df['num_of_isolation_bed'][row],
                    occupied_isolation_bed=df['occupied_isolation_bed'][row],
                    total_tested=df['total_tested'][row],
                    total_positive=df['total_positive'][row],
                    total_death=df['total_death'][row],
                    total_in_isolation=df['total_in_isolation'][row],
                    lat=df['lat'][row],
                    long=df['long'][row],

                    f_5=df['f_5'][row],
                    f_10=df['f_10'][row],
                    f_15=df['f_15'][row],
                    f_20=df['f_20'][row],
                    f_25=df['f_25'][row],
                    f_30=df['f_30'][row],
                    f_35=df['f_35'][row],
                    f_40=df['f_40'][row],
                    f_45=df['f_45'][row],
                    f_50=df['f_50'][row],
                    f_55=df['f_55'][row],
                    f_60=df['f_60'][row],
                    f_65=df['f_65'][row],
                    f_70=df['f_70'][row],
                    f_75=df['f_75'][row],
                    f_80=df['f_80'][row],
                    m_5=df['m_5'][row],
                    m_10=df['m_10'][row],
                    m_15=df['m_15'][row],
                    m_20=df['m_20'][row],
                    m_25=df['m_25'][row],
                    m_30=df['m_30'][row],
                    m_35=df['m_35'][row],
                    m_40=df['m_40'][row],
                    m_45=df['m_45'][row],
                    m_50=df['m_50'][row],
                    m_55=df['m_55'][row],
                    m_60=df['m_60'][row],
                    m_65=df['m_65'][row],
                    m_70=df['m_70'][row],
                    m_75=df['m_75'][row],
                    m_80=df['m_80'][row],
                    male_total=df['male_total'][row],
                    female_total=df['female_total'][row],
                    male_high_risk=df['male_highrisk'][row],
                    female_high_risk=df['female_highrisk'][row],
                    total=df['total'][row],
                    all_high_risk=df['all_highrisk'][row],
                    all_risk_pct=df['all_risk_pct'][row],
                    male_high_pct=df['male_risk_pct'][row],
                    female_high_pct=df['female_risk_pct'][row],

                    data='DryDshosp4hrSums'
                )
                print(row, 'CovidFivew object successfully created')

        except Exception as e:
            print(e)
