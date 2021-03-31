from django.core.management.base import BaseCommand
import pandas as pd
from core.models import Program


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
            prog = [
                Program(
                    partner_id=(df['PARTNER CODE'][row]),
                    name=(df['PROGRAMME NAME'][row]),
                    code=df['Programme Code'][row],
                    total_budget=df['BUDGET (£)'][row],

                ) for row in range(0, upper_range)
            ]
            prog_data = Program.objects.bulk_create(prog)

            if prog_data:
                self.stdout.write('Successfully loaded Partner data ..')
            # for row in range(0, upper_range):
            #     print(df['Partner Name'][row])

        except Exception as e:
            print(e)
