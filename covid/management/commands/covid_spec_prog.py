from django.core.management.base import BaseCommand
import pandas as pd
from core.models import GapaNapa, Province, District
from covid.models import CovidSpecificProgram


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
                print(df['ProvinceID'][row])
                # province = Province.objects.get(code=int(df['ProvinceID'][row]))
                district = District.objects.get(code=int(df['DistrictID'][row]))
                # municipality = GapaNapa.objects.get(code=int(df['Palika'][row]))

                # CovidSpecificProgram.objects.create(
                #     partner=df['1st Tier Partners with ID'][row],
                #     program=df['Programme Name '][row],
                #     component=df['Component Name'][row],
                #     second_tier_partner=df['2nd Tier Partner'][row],
                #     project_status=df['Project Status'][row],
                #     budget=df['Budget'][row],
                #     kathmandu_activity=df['Kathmandu Activity '][row],
                #     delivery_in_lockdown=df['Delivery in Lockdown'][row],
                #     covid_priority_3_12_Months=df['COVID Priority 3_12 Months'][row],
                #     covid_recovery_priority=df['COVID Recovery Priority'][row],
                #     providing_ta_to_local_government=df['Providing TA to Local Government'][row],
                #     providing_ta_to_provincial_government=df['Providing TA to Provincial Government'][row],
                #     sector=df['Broad Sector'][row],
                #     province_id=province,
                #     district_id=district,
                #     municipality_id=municipality.
                # )
                print(row, 'CovidSpecificProgram object successfully created')

        except Exception as e:
            print(e)
