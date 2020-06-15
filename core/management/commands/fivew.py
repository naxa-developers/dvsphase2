from django.core.management.base import BaseCommand
import pandas as pd
from core.models import Project, Program, Partner, FiveW, Province, District, GapaNapa


class Command(BaseCommand):
    help = 'load province data from province.xlsx file'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']

        df = pd.read_csv(path)
        upper_range = len(df)
        print("Wait Data is being Loaded")

        try:
            five = [
                FiveW(
                    supplier_id=Partner.objects.get(code=str(int(df['1st Tier Partner Code'][row]))),
                    # second_tier_partner=Partner.objects.get(code=str(int(df['2nd Tier Partner Code'][row]))),
                    second_tier_partner_name=df['2nd Tier Partner'][row],
                    component_id=Project.objects.get(code=str(df['Component Code'][row])),
                    program_id=Program.objects.get(code=str(int(df['Prog. Code'][row]))),
                    province_id=Province.objects.get(code=str(int(df['Province ID'][row]))),
                    district_id=District.objects.get(code=str(int(df['District ID'][row]))),
                    municipality_id=GapaNapa.objects.get(hlcit_code=df['Palika ID'][row]),
                    status=df['Project Status'][row],
                    allocated_budget=float(df['Budget'][row]),
                    kathmandu_activity=df['Kathmandu Activity'][row],
                    delivery_in_lockdown=df['Delivery in Lockdown'][row],
                    covid_priority_3_12_Months=df['COVID Priority 3-12 Months'][row],
                    covid_recovery_priority=df['COVID Recovery Priority'][row],
                    providing_ta_to_local_government=df['Providing TA to Local Government'][row],
                    providing_ta_to_provincial_government=df['Providing TA to Provincial Government'][row],

                ) for row in range(0, upper_range)
            ]
            five_data = FiveW.objects.bulk_create(five)

            if five_data:
                self.stdout.write('Successfully loaded Partner data ..')
            # for row in range(0, upper_range):
            #     print(df['1st Tier Partner Code'][row])
            #     print(Partner.objects.get(code=str(int(df['1st Tier Partner Code'][row]))))


        except Exception as e:
            print(e)
