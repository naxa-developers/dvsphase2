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
                    indicator=Indicator.objects.get(indicator=str((df['indicators'][row]).strip())),
                    gapanapa=GapaNapa.objects.get(name=str((df['paulika_name'][row]).capitalize().strip())),
                    value=float(df['value'][row]),

                ) for row in range(0, upper_range)
            ]
            indicator_data = IndicatorValue.objects.bulk_create(indicator_value)

            if indicator_data:
                self.stdout.write('Successfully loaded Indicator Value  ..')
                # print((df['paulika_name'][row]).capitalize())
                # a = GapaNapa.objects.get(name=str((df['paulika_name'][row]).capitalize().strip()))
                # print(a)
                # print((df['indicators'][row]).strip())
                # a = Indicator.objects.get(indicator=str((df['indicators'][row]).strip()))
                # print(a)


        except Exception as e:
            print(e)
