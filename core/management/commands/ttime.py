from django.core.management.base import BaseCommand
import pandas as pd
from core.models import TravelTime, GapaNapa


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
            # for row in range(0, upper_range):
            #     print((df['adm2_code'][row]))
            #     a = GapaNapa.objects.get(hlcit_code=str((df['adm2_code'][row]).strip()))
            #     print(a)

            ttime = [
                TravelTime(
                    gapanapa=GapaNapa.objects.get(hlcit_code=df['adm2_code'][row]),
                    population=(df['adm2_pop'][row]),
                    category_population=df['cat_pop'][row],
                    season=df['season'][row],
                    geography=df['geog'][row],
                    travel_value=df['trav_value'][row],

                ) for row in range(0, upper_range)
            ]

            ttime_data = TravelTime.objects.bulk_create(ttime)

            if ttime_data:
                self.stdout.write('Successfully loaded Time Travel ..')


        except Exception as e:
            print(e)
