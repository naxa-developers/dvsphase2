from django.core.management.base import BaseCommand
import pandas as pd
from core.models import Project, Program


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
            proj = [
                Project(
                    program_id=Program.objects.get(code=df['Program Code'][row]),
                    name=(df['Component Name'][row]).strip(),
                    code=df['Component Code'][row],

                ) for row in range(0, upper_range)
            ]
            proj_data = Project.objects.bulk_create(proj)

            if proj_data:
                self.stdout.write('Successfully loaded Partner data ..')
            # for row in range(0, upper_range):
            #     print(df['Program Code'][row])
            #     print(Program.objects.get(code=df['Program Code'][row]))


        except Exception as e:
            print(e)