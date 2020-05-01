from django.core.management.base import BaseCommand
import pandas as pd
from core.models import Indicator, IndicatorValue, GapaNapa


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
            indicator_value = [
                IndicatorValue(
                    indicator_id=Indicator.objects.get(indicator='household_affected_covid'),
                    gapanapa_id=GapaNapa.objects.get(hlcit_code=df['HLCIT_CODE'][row]),
                    value=float(df['value'][row]),

                ) for row in range(0, upper_range)
            ]
            indicator_data = IndicatorValue.objects.bulk_create(indicator_value)

            if indicator_data:
                self.stdout.write('Successfully loaded Indicator Value  ..')
            # for row in range(0, upper_range):
            #     print(df['HLCIT_CODE'][row])
            #     GapaNapa.objects.get(hlcit_code=df['HLCIT_CODE'][row])


        except Exception as e:
            print(e)
