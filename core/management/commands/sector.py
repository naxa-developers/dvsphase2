from django.core.management.base import BaseCommand
import pandas as pd
from core.models import Sector, SubSector


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

            sector = [
                Sector(
                    name=df['Broad Sectors'][row],

                ) for row in range(0, upper_range)
            ]

            sector_data = Sector.objects.bulk_create(sector)

            if sector_data:
                self.stdout.write('Successfully loaded Sub sector data ..')


        except Exception as e:
            print(e)
