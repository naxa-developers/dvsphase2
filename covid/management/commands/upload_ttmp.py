from django.core.management.base import BaseCommand
import pandas as pd
from core.models import Indicator, IndicatorValue, GapaNapa, Partner, Program, Project, Province, District
from covid.models import Ttmp


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
                print(row,df['1st Tier Partners'][row])
                print(row,df['Programme Code'][row])
                print(row, df['Province_ID'][row])
                partner = Partner.objects.get(name__icontains=df['1st Tier Partners'][row])
                supplier = Partner.objects.get(name__icontains=df['1st Tier Partners'][row])
                program = Program.objects.get(code=int(df['Programme Code'][row]))
                province = Province.objects.get(code=int(df['Province_ID'][row]))
                district = District.objects.get(code=int(df['District_ID'][row]))
                municipality = GapaNapa.objects.get(code=int(df['Palika_ID'][row]))

                ttmp = Ttmp.objects.create(
                    partner_id=partner,
                    supplier_id=supplier,
                    program_id=program,
                    project_code=df['Project/Component Code'][row],
                    project_name=df['Project Name'][row],
                    province_id=province,
                    district_id=district,
                    municipality_id=municipality
                )

                print('ttmp object successfully created')
                
        except Exception as e:
            print(e)
