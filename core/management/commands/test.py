from django.core.management.base import BaseCommand
import pandas as pd
from core.models import FiveW, Project, District, GapaNapa, Partner, Program, Province
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseCommand):
    help = 'load province data from province.xlsx file'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        df = pd.read_csv(path)
        upper_range = len(df)
        print("Wait Data is being Loaded")
        fivew_correct = []
        fivew_incorrect = []
        success_count = 0
        for row in range(0, upper_range):
            try:
                fivew_correct.append(FiveW(
                    supplier_id=Partner.objects.get(code=df['1st TIER PARTNER CODE'][row]),
                    second_tier_partner_name=df['2nd TIER PARTNER'][row],
                    component_id=Project.objects.get(code=df['Project/Component Code'][row]),
                    program_id=Program.objects.get(code=df['Programme Code'][row]),
                    province_id=Province.objects.get(code=df['PROVINCE.CODE'][row]),
                    district_id=District.objects.get(code=df['D.CODE'][row]),
                    municipality_id=GapaNapa.objects.get(hlcit_code=df['PALIKA.Code'][row]),
                    status=df['PROJECT STATUS'][row],
                    reporting_line_ministry=df['REPORTING LINE MINISTRY'][row],
                    contact_name=df['CONTACT NAME'][row],
                    designation=df['DESIGNATION'][row],
                    contact_number=df['CONTACT NUMBER'][row],
                    email=df['EMAIL'][row],
                    remarks=df['REMARKS'][row],
                ))
                success_count += 1
            except Exception as e:
                incorrect = df.iloc[row]
                fivew_incorrect.append(incorrect)
        if fivew_incorrect:
            merged = pd.concat(fivew_incorrect)
            merged.to_csv('incorrect_csv_data/errordata.csv')
        FiveW.objects.bulk_create(fivew_correct)
        print(str(success_count) + "Data Successfully Uploaded")
