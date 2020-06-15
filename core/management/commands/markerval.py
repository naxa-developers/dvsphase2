from django.core.management.base import BaseCommand
import pandas as pd
from core.models import MarkerCategory, MarkerValues


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
            #     print((df['sector'][row]))
            #     a = Sector.objects.get(sector_name=str((df['sector'][row]).strip()))
            #     print(a)

            marker = [
                MarkerValues(
                    marker_category_id=MarkerCategory.objects.get(name=str((df['Markers'][row]).strip())),
                    value=(df['Value'][row]).strip(),

                ) for row in range(0, upper_range)
            ]

            marker_data = MarkerValues.objects.bulk_create(marker)

            if marker_data:
                self.stdout.write('Successfully loaded marker data ..')


        except Exception as e:
            print(e)
