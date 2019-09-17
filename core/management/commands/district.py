from django.core.management.base import BaseCommand
import pandas as pd
from core.models import Province, District


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
            district = [
                District(
                    province=Province.objects.get(province_code=df['Province_id'][row]),
                    district_name=(df['District_name'][row]).capitalize().strip(),
                    district_code=int(df['District_id'][row]),

                ) for row in range(0, upper_range)
            ]
            district_data = District.objects.bulk_create(district)

            if district_data:
                self.stdout.write('Successfully loaded District data ..')


        except Exception as e:
            print(e)
