from django.core.management.base import BaseCommand
import pandas as pd
from core.models import Indicator, IndicatorValue, GapaNapa, District
from django.core.exceptions import ObjectDoesNotExist


def gapanapa(code):
    try:
        obj = GapaNapa.objects.get(hlcit_code=str(code))
    except ObjectDoesNotExist:
        obj = None
    return obj


def valuedata(val):
    try:
        data = float(val)
    except:
        data = 0
    return data


class Command(BaseCommand):
    help = 'load province data from province.xlsx file'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']

        df1 = pd.read_csv(path)
        df = df1.fillna('')
        upper_range = len(df)
        print("Wait Data is being Loaded")
        try:
            indicator_value = [
                IndicatorValue(
                    indicator_id=Indicator.objects.get(indicator=df['Indicators'][row].strip()),
                    gapanapa_id=gapanapa(df['Hlcit Id'][row]),
                    national_average=float(df['National Average '][row]),
                    province_average=float(df['Province average '][row]),
                    district_average=float(df['District Average '][row]),
                    value=valuedata(df['Value'][row]),

                ) for row in range(0, upper_range)
            ]
            indicator_data = IndicatorValue.objects.bulk_create(indicator_value)

            if indicator_data:
                self.stdout.write('Successfully loaded Indicator Value  ..')

        except Exception as e:
            print(e)
