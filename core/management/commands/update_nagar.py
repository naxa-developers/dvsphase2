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
                print(df['HLCIT_CODE'][row])
                # a = District.objects.get(district_name=str((df['district'][row]).capitalize().strip()))
                # print(a)
                # palika_update = GapaNapa.objects.filter(hlcit_code=df['adm2_code'][row]).update(
                #     population=float(df['adm2_pop'][row]),
                #     geography=(df['geog'][row]).strip())

                palika_update = GapaNapa.objects.filter(hlcit_code=df['HLCIT_CODE'][row]).update(
                    code=int(df['munid'][row]))

                if palika_update:
                    self.stdout.write('Successfully  updated data ..')

                # if (df['hlcit_code'][row] == '524 1 14 4 003'):
                #
                #     palika_update = GapaNapa.objects.filter(hlcit_code=df['hlcit_code'][row]).update(
                #         boundary=GEOSGeometry(df['geom'][row]))
                #
                #     if palika_update:
                #         self.stdout.write('Successfully  updated data ..')
                # else:
                #     print('else')



        except Exception as e:
            print(e)
