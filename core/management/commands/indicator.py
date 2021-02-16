

from django.core.management.base import BaseCommand
import os
import pandas as pd

from core.models import Indicator


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
        upper_range = len(df)
        try:
            indicator = [
                Indicator(
                    indicator=(df['indicators'][row]).strip(),
                    full_title=df['Fulltitle'][row],
                    abstract=df['Abstract'][row],
                    category=(df['Category'][row]).strip(),
                    source=df['Source'][row],
                    federal_level=df['Level'][row],

                ) for row in range(0, upper_range)
            ]
            indicator_data = Indicator.objects.bulk_create(indicator)
            print(indicator_data)
            if indicator_data:
                self.stdout.write('Successfully loaded Indicator data ..')
        except Exception as e:
            print(e)
