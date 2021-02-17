from django.core.management.base import BaseCommand
import pandas as pd
from core.models import Indicator, IndicatorValue, GapaNapa, District
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseCommand):
    help = 'load province data from province.xlsx file'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        # print(path)
        # print(os.path.exists("/home/sumit/django_projects/dvs/data_csv"))
        # print(os.path.isfile(path))
        df = pd.read_csv(path)
        # print(df['Level'][0])
        # print(len(df))
        upper_range = list(df.columns)
        category_name = ((path.split('/'))[-1]).replace('.csv', '')

        not_cols = ['District', 'district', 'Name of municipalities', 'Name of Municipalities', 'CBS_CODE',
                    'HLCIT_CODE', 'Province', 'province', 'Palika',
                    'palika', 'CBS_Code', 'District ', 'code', 'cbs code']

        try:
            indicator = [
                Indicator(
                    indicator=col,
                    full_title=col,
                    # abstract=df['Abstract'][row],
                    category=category_name,
                    # source=df['Source'][row],
                    federal_level='All',

                ) for col in upper_range if not col in not_cols
            ]
            indicator_data = Indicator.objects.bulk_create(indicator)
            if indicator_data:
                self.stdout.write('Successfully loaded Indicator data ..')
        except Exception as e:
            print(e)
