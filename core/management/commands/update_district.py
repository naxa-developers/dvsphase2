from django.core.management.base import BaseCommand
import pandas as pd
from core.models import Province, District, GapaNapa
from django.contrib.gis.geos import GEOSGeometry


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
                print(df['hlcitId'][row])

                # palika_update = District.objects.filter(code=df['id'][row]).update(
                #     boundary=GEOSGeometry(df['geom'][row]))

                palika_update = District.objects.filter(code=df['hlcitId'][row]).update(
                    n_code=int(df['districtId'][row]))

            if palika_update:
                self.stdout.write('Successfully  updated data ..')





        except Exception as e:
            print(e)
