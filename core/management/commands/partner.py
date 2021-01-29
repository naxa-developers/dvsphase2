from django.core.management.base import BaseCommand
import pandas as pd
from core.models import Partner


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
            part = [
                Partner(
                    name=(df['1st TIER PARTNER'][row]).strip(),
                    code=df['1st TIER PARTNER CODE'][row],

                ) for row in range(0, upper_range)
            ]
            partner_data = Partner.objects.bulk_create(part)

            if partner_data:
                self.stdout.write('Successfully loaded Partner data ..')
            # for row in range(0, upper_range):
            #     print(df['Partner Name'][row])

        except Exception as e:
            print(e)
