from django.core.management.base import BaseCommand
import pandas as pd
from core.models import Program, MarkerCategory, MarkerValues


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
            for row in range(0, upper_range):
                a1 = Program.objects.get(code=df['Programme Code'][row])
                m1 = MarkerCategory.objects.get(name=df['Category'][row])
                m2 = MarkerValues.objects.get(marker_category_id=m1, value=df['Sub-Category'][row])
                # data = a1.marker_category.add(m1)
                data = a1.marker_value.add(m2)
                # print(m2.value, m2.marker_category_id)

            if data:
                self.stdout.write('Successfully loaded  data ..')


        except Exception as e:
            print(e)
